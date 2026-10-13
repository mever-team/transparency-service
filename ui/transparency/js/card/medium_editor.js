let editor;
let turndownService = null;
let markedInstance = null;

////////////////////////////////////////////
// Helpers
////////////////////////////////////////////
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


function insertTable() {
    const selection = window.getSelection();

    if (!selection || selection.rangeCount === 0) return;

    const range = selection.getRangeAt(0);

    // Make sure the cursor is inside the MediumEditor instance
    const editable = range.commonAncestorContainer.nodeType === Node.TEXT_NODE
        ? range.commonAncestorContainer.parentElement.closest('.medium-editor-element')
        : range.commonAncestorContainer.closest('.medium-editor-element');

    if (!editable) return;

    const table = `
        <table>
            <thead>
                <tr>
                    <th>Header 1</th>
                    <th>Header 2</th>
                    <th>Header 3</th>
                </tr>
            </thead>
            <tbody>
                <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
                <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
                <tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>
            </tbody>
        </table>
        <p><br></p>
    `;

    // Focus the editor and restore the cursor selection
    editable.focus();
    selection.removeAllRanges();
    selection.addRange(range);

    // Native insertion helps preserve Ctrl+Z undo behavior
    document.execCommand('insertHTML', false, table);

    // Notify MediumEditor that the content changed
    if (window.jQuery) {
        window.jQuery(editable).trigger('input');
        window.jQuery(editable).trigger('editableInput');
    }
}

////////////////////////////////////////////
// Custom MediumEditor extension
////////////////////////////////////////////

var TableButton = MediumEditor.Extension.extend({
    name: 'table',

    init: function () {
        this.button = document.createElement('button');
        this.button.classList.add('medium-editor-action');
        this.button.innerHTML = '<i class="fa-solid fa-table"></i>';
        this.button.title = 'Table';
        this.button.onclick = this.handleClick.bind(this);
    },
    getButton: function () {
        return this.button;
    },
    handleClick: function (event) {
        this.action();
    },
    action: function () {
        insertTable();
    }

})

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

////////////////////////////////////////////
// Init Converters
////////////////////////////////////////////
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

////////////////////////////////////////////
// Exports
////////////////////////////////////////////
export function htmlToMarkdown(html) {
    initConverters();

    if (!turndownService) return html;
    if (!html || typeof html !== 'string') return '';

    const container = document.createElement('div');
    container.innerHTML = html;

    let markdown = turndownService.turndown(container.innerHTML);
    markdown = markdown.replace(/(\|.*\|)\n\n(?=\|)/g, '$1\n');

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
            'codeblock',
            'table'
        ],
        static: true,
        updateOnEmptySelection: true
        }, 
        extensions: {
            codeblock: new CodeBlockButton(),
            table: new TableButton()
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

//////////////////////////////////////
// Table functionality
//////////////////////////////////////

export function initTableControls() {
    $('.field-value[contenteditable="true"]').each(function () {
        const editable = this;
        const $editor = $(editable);

        if ($editor.data('tableControlsInitialized')) return;
        $editor.data('tableControlsInitialized', true);

        // show table toolbar
        $editor.on(
            'mousedown.tableControls focusin.tableControls',
            'table td, table th',
            function () {
                const $controls = ensureTableActionRow();

                if (!$controls) return;

                $controls.data({
                    activeEditor: editable,
                    activeTable: this.closest('table'),
                    activeCell: this
                });

                $controls.show();
                requestAnimationFrame(() => {
                    if (editor) editor.checkSelection();
                });
            }
        );

        // hide table toolabar
        $editor.on('mousedown.tableControls', function (event) {
            if ($(event.target).closest('table td, table th').length) {
                return;
            }

            ensureTableActionRow()?.hide();
        });
    });
}

// medium editor table actions
function ensureTableActionRow() {
    const $toolbar = $('.medium-editor-toolbar').first();

    if (!$toolbar.length) return null;

    let $controls = $toolbar.children('.medium-editor-table-controls');

    if ($controls.length) {
        const observer = new MutationObserver(() => {
            requestAnimationFrame(() => {
                if (editor) editor.checkSelection();
            });
        });

        observer.observe($controls[0], {
            attributes: true,
            attributeFilter: ['style', 'class']
        });
    }

    if (!$controls.length) {
        $controls = $('<div>', {
            class: 'medium-editor-table-controls'
        }).hide();

        const actions = [
            ['+ Row', 'add-row'],
            ['- Row', 'remove-row'],
            ['+ Column', 'add-column'],
            ['- Column', 'remove-column'],
            ['Delete Table', 'delete-table']
        ];

        actions.forEach(([label, action]) => {
            $('<button>', {
                type: 'button',
                text: label,
                title: label
            })
                .attr('data-table-action', action)
                .appendTo($controls);
        });

        $toolbar.append($controls);

        // Keep the editor selection when clicking a table action.
        $controls.on('mousedown.tableControls', 'button', function (event) {
            event.preventDefault();
        });

        $controls.on('mousedown.tableControls', 'button', function () {
            const action = $(this).attr('data-table-action');

            const editor = $controls.data('activeEditor');
            const table = $controls.data('activeTable');
            const cell = $controls.data('activeCell');

            if (!editor || !table || !table.isConnected) {
                $controls.hide();
                requestAnimationFrame(() => {
                    if (editor) editor.checkSelection();
                });
                return;
            }

            if (action !== 'delete-table' && !cell) return;

            const tableIndex = Array.from(
                editor.querySelectorAll('table')
            ).indexOf(table);

            const rowIndex = cell?.parentElement.rowIndex ?? 0;
            const columnIndex = cell?.cellIndex ?? 0;

            if (action === 'delete-table') {
                deleteTableUndoably(table);
                $controls.hide();
                requestAnimationFrame(() => {
                    if (editor) editor.checkSelection();
                });

                $controls.removeData(
                    'activeEditor activeTable activeCell'
                );

                notifyEditorChanged(editor);
                return;
            }

            if (action === 'remove-row' && table.rows.length <= 1) return;

            if (
                action === 'remove-column' &&
                cell.parentElement.cells.length <= 1
            ) return;

            const success = replaceTableUndoably(table, replacement => {
                switch (action) {
                    case 'add-row': {
                        const row = replacement.rows[rowIndex];
                        if (!row) return;

                        const newRow = document.createElement('tr');

                        Array.from(row.cells).forEach(existingCell => {
                            const newCell = document.createElement(
                                existingCell.tagName.toLowerCase()
                            );

                            newCell.innerHTML = '&nbsp;';
                            newRow.appendChild(newCell);
                        });

                        row.after(newRow);
                        break;
                    }

                    case 'remove-row':
                        replacement.rows[rowIndex]?.remove();
                        break;

                    case 'add-column':
                        Array.from(replacement.rows).forEach(row => {
                            const existingCell = row.cells[columnIndex];

                            const tag = existingCell
                                ? existingCell.tagName.toLowerCase()
                                : row.parentElement.tagName === 'THEAD'
                                    ? 'th'
                                    : 'td';

                            const newCell = document.createElement(tag);
                            newCell.innerHTML = '&nbsp;';

                            if (existingCell) {
                                existingCell.after(newCell);
                            } else {
                                row.appendChild(newCell);
                            }
                        });
                        break;

                    case 'remove-column':
                        Array.from(replacement.rows).forEach(row => {
                            row.cells[columnIndex]?.remove();
                        });
                        break;
                }
            });

            if (!success) return;

            // Find the replacement table at its original position.
            const newTable = editor.querySelectorAll('table')[tableIndex];

            if (!newTable) {
                $controls.hide();
                requestAnimationFrame(() => {
                    if (editor) editor.checkSelection();
                });
                return;
            }

            const targetRow = newTable.rows[
                Math.min(
                    action === 'add-row' ? rowIndex + 1 : rowIndex,
                    newTable.rows.length - 1
                )
            ];

            const targetColumn = Math.min(
                action === 'add-column'
                    ? columnIndex + 1
                    : columnIndex,
                (targetRow?.cells.length ?? 1) - 1
            );

            const newCell = targetRow?.cells[targetColumn];

            $controls.data({
                activeEditor: editor,
                activeTable: newTable,
                activeCell: newCell ?? null
            });

            if (newCell) {
                $controls.data({
                    activeEditor: editor,
                    activeTable: newTable,
                    activeCell: newCell
                });

                focusCell(newCell);
                $controls.show();
                requestAnimationFrame(() => {
                    if (editor) editor.checkSelection();
                });
            } else {
                $controls.hide();
                requestAnimationFrame(() => {
                    if (editor) editor.checkSelection();
                });
            }

            notifyEditorChanged(editor);
        });
    }

    return $controls;
}

// make table action buttons respect ctrl+z
function replaceTableUndoably(table, mutate) {
    const replacement = table.cloneNode(true);
    mutate(replacement);

    const selection = window.getSelection();
    const range = document.createRange();

    range.selectNode(table);
    selection.removeAllRanges();
    selection.addRange(range);

    return document.execCommand(
        'insertHTML',
        false,
        replacement.outerHTML
    );
}

function deleteTableUndoably(table) {
    const selection = window.getSelection();
    const range = document.createRange();

    range.selectNode(table);
    selection.removeAllRanges();
    selection.addRange(range);

    document.execCommand('delete', false, null);
}

function notifyEditorChanged(editable) {
    $(editable).trigger('input');
    $(editable).trigger('editableInput');
}

function focusCell(cell) {
    if (!cell) return;

    cell.focus?.();

    const range = document.createRange();
    const selection = window.getSelection();

    range.selectNodeContents(cell);
    range.collapse(true);

    selection.removeAllRanges();
    selection.addRange(range);
}