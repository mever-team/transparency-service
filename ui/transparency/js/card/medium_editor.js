let editor;
let turndownService = null;
let markedInstance = null;

// Custom MediumEditor extension for inserting code blocks
function getHighestPreFromNode(node) {
    let current = node;
    let highestPre = null;

    while (current) {
        if (current.nodeType === 1 && current.tagName === "PRE") {
        highestPre = current;
        }
        current = current.parentNode;
    }

    return highestPre;
}
function getHighestPreFromCursor() {
    const selection = window.getSelection();
    if (!selection.rangeCount) return null;
    let node = selection.anchorNode;
    if (node.nodeType === 3) {
        node = node.parentElement;
    }
    return getHighestPreFromNode(node);
}
var CodeBlockButton = MediumEditor.Extension.extend({
    name: 'codeblock',

    init: function () {
        this.button = document.createElement('button');
        this.button.classList.add('medium-editor-action');
        this.button.innerHTML = '&lt;/&gt;';
        this.button.title = 'Code Block';
        this.button.onclick = this.handleClick.bind(this);
    },

    getButton: function () {
        return this.button;
    },

    handleClick: function (event) {
        this.action();
    },

    checkState: function (node) {
        var sel = window.getSelection();
        if (!sel.rangeCount) {
            this.button.classList.remove('medium-editor-button-active');
            return false;
        }

        var range = sel.getRangeAt(0);
        var container = range.commonAncestorContainer;
        var el = container.nodeType === 3 ? container.parentElement : container;
        var inside = !!el.closest('pre');

        this.button.classList.toggle('medium-editor-button-active', inside);

        // disable other buttons
        var toolbar = this.base.getExtensionByName('toolbar');
        if (toolbar && toolbar.getToolbarElement) {
            var buttons = toolbar.getToolbarElement().querySelectorAll('button');

            buttons.forEach((btn) => {
                if (btn === this.button) {
                    btn.disabled = false;
                } else {
                    btn.disabled = inside;
                }
                // console.log(btn);
            });
        }
        return inside;
    },

    // Toggle behavior
    action: function () {
        var editor = this.base;
        var selection = window.getSelection();
        if (!selection || selection.rangeCount === 0) return;

        var range = selection.getRangeAt(0);
        var container = range.commonAncestorContainer;
        var el = container.nodeType === 3 ? container.parentElement : container;
        var preElement = el.closest('pre');

        if (preElement) {
            const parentPre = getHighestPreFromCursor();
            const range = document.createRange();
            range.selectNodeContents(parentPre);
            const selection = window.getSelection();
            selection.removeAllRanges();
            selection.addRange(range);
            document.execCommand('formatBlock', false, 'div');
            
        } else {
            document.execCommand('formatBlock', false, 'pre');
            // preElement = window.getSelection().focusNode.parentNode;
            if (selection.rangeCount > 0) {
                let node = selection.getRangeAt(0).startContainer;
                if (node.nodeType === Node.TEXT_NODE) {
                    node = node.parentElement;
                }
                preElement = node.closest('pre');
            }
            preElement.innerHTML = preElement.innerHTML.replaceAll("<br>", "\n");
            hljs.highlightElement(preElement);
            preElement.setAttribute('spellcheck', 'false');
            preElement.setAttribute('autocorrect', 'off');
            preElement.setAttribute('autocapitalize', 'off');
            preElement.setAttribute('translate', 'no');
        }

        // Notify the editor that content changed
        var editable = editor.elements[0];
        if (editable) {
            $(editable).trigger('input');
            $(editable).trigger('editableInput');
        }
        this.checkState();
    }
});

function initConverters() {
    function getPreText(node) {
        let text = '';
        for (const child of node.childNodes) {
            if (child.nodeType === Node.TEXT_NODE) {
                text += child.textContent;
            } else if (child.nodeType === Node.ELEMENT_NODE) {
                if (child.tagName === 'BR') {
                    text += '\n';
                } else {
                    text += getPreText(child);
                }
            }
        }
        return text;
    }

    // ---------- Turndown ----------
    if (typeof TurndownService !== 'undefined' && !turndownService) {
        turndownService = new TurndownService({
            headingStyle: 'atx',
            codeBlockStyle: 'fenced'
        });
        turndownService.use(turndownPluginGfm.tables);
        turndownService.keep(['sub', 'sup', 'u', 'ins']);

        // Custom rule for <pre>
        turndownService.addRule('pre', {
            filter: 'pre',
            replacement: function(content, node) {
                const codeText = getPreText(node);
                return '```\n' + codeText + '\n```';
            }
        });
    }

    // ---------- Marked ----------
    if (typeof marked !== 'undefined' && !markedInstance) {
        markedInstance = marked;
        markedInstance.setOptions({ breaks: true, gfm: true });

        // Renderer to output plain <pre>
        const renderer = {
            code(token) {
                const codeText = (token.text || token);
                const language = token.lang || '';
                const langAttr = language ? ` class="language-${language}"` : '';
                return `<pre${langAttr}>${codeText}</pre>`;
            }
        };
        markedInstance.use({ renderer });

    }
}

export function htmlToMarkdown(html) {
    initConverters();

    if (!turndownService) return html;
    if (!html || typeof html !== 'string') return '';

    const container = document.createElement('div');
    container.innerHTML = html;

    console.log(html);
    let markdown = turndownService.turndown(container.innerHTML);
    markdown = markdown.replace(/(\|.*\|)\n\n(?=\|)/g, '$1\n');
    console.log(markdown);

    return markdown;
}

export function markdownToHtml(md) {
    initConverters();
    if (!markedInstance) return md;
    if (!md || typeof md !== 'string') return '';
    return markedInstance.parse(md);
}

export function initMediumEditor(){
    editor = new MediumEditor('span.editable', {
    placeholder: false,

    toolbar: {
        buttons: [
            'bold',
            'italic',
            'underline',
            'anchor',
            // 'h2',
            // 'h3',
            'quote',
            'orderedlist',
            'unorderedlist',
            'codeblock'
        ],
        static: true,
        updateOnEmptySelection: true
        }, 
        extensions: {
            codeblock: new CodeBlockButton()
        }
    });

    editor.subscribe('showToolbar', function() {
        var $toolbar = $('.medium-editor-toolbar');
        if ($toolbar.length && !$toolbar.find('.undo-hint').length) {
            $('<div class="undo-hint">⌨️ Ctrl+Z to undo</div>')
                .prependTo($toolbar);
        }
});

editor.subscribe('hideToolbar', function() {
    $('.medium-editor-toolbar .undo-hint').remove();
});
}