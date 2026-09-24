function compressHistory(historyEdges, hidden, nodeIds) {
    const visible = new Set([...nodeIds].filter(id => !hidden.has(id)));
    if (visible.size <=1 ) return {compactHistory: [], newRootId: null};
    const newRootId = Math.min(...visible);   // smallest visible id → new root
    const children = new Map();
    for (const [u, v, msg] of historyEdges) {
        if (!children.has(u)) children.set(u, []);
        children.get(u).push({id: v, msg});
    }
    const compactHistory = [];
    const stack = [{visibleAncestor: newRootId, node: newRootId}];
    const visited = new Set();
    while (stack.length) {
        const {visibleAncestor, node} = stack.pop();
        if (visited.has(node)) continue;
        visited.add(node);
        const out = children.get(node) || [];
        for (const {id: nb, msg} of out) {
            if (hidden.has(nb)) {
                stack.push({visibleAncestor, node: nb});
                continue;
            }
            compactHistory.push([visibleAncestor, nb, msg]);
            stack.push({visibleAncestor: nb, node: nb});
        }
    }
    return {compactHistory, newRootId};
}

function relaxLayout(yPos, depth, adj, hasLabel, Y_SPACING) {
    const byDepth = new Map();
    depth.forEach((d, id) => {if (!byDepth.has(d)) byDepth.set(d, []);byDepth.get(d).push(id);});
    const MIN_GAP = new Map();
    depth.forEach((_, id) => MIN_GAP.set(id, hasLabel.has(id) ? Y_SPACING * 1.6 : Y_SPACING));
    const ITERATIONS = 300;
    const SPRING_K = 0.03;
    const REPEL_K = 1.5;
    for (let it = 0; it < ITERATIONS; it++) {
        const force = new Map();
        depth.forEach((_, id) => force.set(id, 0));
        adj.forEach((neighbors, u) => {
            neighbors.forEach(v => {
                if (v <= u) return; // each edge once
                const diff = yPos.get(v) - yPos.get(u);
                const pull = diff * SPRING_K;
                force.set(u, force.get(u) + pull);
                force.set(v, force.get(v) - pull);
            });
        });
        byDepth.forEach(ids => {
            const sorted = [...ids].sort((a, b) => yPos.get(a) - yPos.get(b));
            for (let i = 0; i < sorted.length - 1; i++) {
                const a = sorted[i], b = sorted[i + 1];
                const gap = yPos.get(b) - yPos.get(a);
                const needed = (MIN_GAP.get(a) + MIN_GAP.get(b)) / 2;
                if (gap < needed) {
                    const push = (needed - gap) * REPEL_K;
                    force.set(a, force.get(a) - push);
                    force.set(b, force.get(b) + push);
                }
            }
        });
        depth.forEach((_, id) => yPos.set(id, yPos.get(id) + force.get(id)));
    }
}

function renderHistoryGraph(history, currentId, container) {
    //console.log(history);
    let compareMode = false;
    const compareToId = Number(new URLSearchParams(window.location.search).get('compareto')) || null;

    let node_info = history.info;
    history = history.edges; // dict from node id to tuple (username, version)
    if (!history || history.length === 0) return;
    if (history.length<2) return;
    const nodeIds = new Set();
    history.forEach(([u, v]) => {
        nodeIds.add(u);
        nodeIds.add(v);
    });
    const hidden = new Set();
    nodeIds.forEach(u => {if(!node_info[u][1].length && node_info[u][0]!==loggedUser) hidden.add(u)});
    let rootId = Math.min(...nodeIds);
    const {compactHistory, newRootId} = compressHistory(history, hidden, nodeIds);
    history = compactHistory;
    rootId = newRootId;
    if (history.length<2) return;

    const btn = document.createElement('button');
    btn.className = 'compare-toggle-btn';
    btn.textContent = 'select to compare: off';
    $(btn).on('click', () => {
        compareMode = !compareMode;
        btn.classList.toggle('active', compareMode);
        btn.textContent = compareMode?'select to compare: on':'select to compare: off'
    });
    container.appendChild(btn);


    const X_SPACING = 200;
    const Y_SPACING = 35;
    const NODE_RADIUS = 10;
    const adj = new Map();
    const edges = [];
    const selfLabels = new Map();

    history.forEach(([u, v, msg]) => {
        if(u === v) {
            if (msg) selfLabels.set(u, {
                line1: (node_info[u][1].length===0?"[DRAFT] ":(node_info[u][1]!==msg)?(node_info[u][1]+" "):"")+msg,
                line2: "by " + node_info[u][0]
            });return;
        }
        if (!adj.has(u)) adj.set(u, new Set());
        if (!adj.has(v)) adj.set(v, new Set());
        adj.get(u).add(v);
        adj.get(v).add(u);
        edges.push([u, v, msg || ""]);
    });

    const depth = new Map([[rootId, 0]]);
    const tree = new Map([[rootId, []]]);
    const queue = [rootId];
    while (queue.length) {
        const n = queue.shift();
        const d = depth.get(n);
        for (const nb of adj.get(n) || []) {
            if (depth.has(nb)) continue;
            depth.set(nb, d + 1);
            tree.get(n).push(nb);
            tree.set(nb, []);
            queue.push(nb);
        }
    }

    const yPos = new Map([[rootId, 0]]);

    function layout(node) {
        const kids = tree.get(node);
        if (!kids || kids.length === 0) return;
        if (kids.length === 1) {
            yPos.set(kids[0], yPos.get(node));
            layout(kids[0]);
            return;
        }
        kids.forEach((child, i) => {
            const offset = Math.ceil((i + 1) / 2) * Y_SPACING;
            const sign = i % 2 === 0 ? -1 : 1;
            yPos.set(child, yPos.get(node) + sign * offset);
            layout(child);
        });
    }

    layout(rootId);
    relaxLayout(yPos, depth, adj, selfLabels, Y_SPACING);

    const ys = Array.from(yPos.values());
    const minY = Math.min(...ys);
    const LABEL_HEADROOM = 40; // room above the topmost node for its two-line label
    yPos.forEach((v, k) => yPos.set(k, v - minY + LABEL_HEADROOM));

    const maxDepth = Math.max(...depth.values());
    const width = (maxDepth + 1) * X_SPACING + 80;
    const height = Math.max(...yPos.values()) + 20;

    const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("width", width);
    svg.setAttribute("height", height);
    svg.classList.add("history-graph");

    const defs = document.createElementNS(svg.namespaceURI, "defs");
    defs.innerHTML = `
      <marker id="arrow-head"
              markerWidth="10"
              markerHeight="10"
              refX="15"
              refY="3"
              orient="auto"
              markerUnits="strokeWidth">
        <path d="M0,0 L9,3 L0,6 Z" fill="#79CFDC"/>
      </marker>`;
    svg.appendChild(defs);

    edges.forEach(([u, v, msg]) => {
        if (!depth.has(u) || !depth.has(v)) return;
        const x1 = depth.get(u) * X_SPACING + 40;
        const y1 = yPos.get(u);
        const x2 = depth.get(v) * X_SPACING + 40;
        const y2 = yPos.get(v);
        const line = document.createElementNS(svg.namespaceURI, "line");
        line.setAttribute("x1", x1);
        line.setAttribute("y1", y1);
        line.setAttribute("x2", x2);
        line.setAttribute("y2", y2);
        line.setAttribute("marker-end", "url(#arrow-head)");
        line.classList.add("edge");
        svg.appendChild(line);
        if (msg) {
            const t = document.createElementNS(svg.namespaceURI, "text");
            t.setAttribute("x", (x1 + x2) / 2);
            t.setAttribute("y", (y1 + y2) / 2 - 8);
            t.setAttribute("text-anchor", "middle");
            t.setAttribute("pointer-events", "none");
            t.classList.add("edge-label");
            t.textContent = msg;
            svg.appendChild(t);
        }
    });

    depth.forEach((d, id) => {
        const x = d * X_SPACING + 40;
        const y = yPos.get(id)+6;
        const g = document.createElementNS(svg.namespaceURI, "g");
        g.classList.add("node");
        const c = document.createElementNS(svg.namespaceURI, "circle");
        c.setAttribute("cx", x);
        c.setAttribute("cy", y);
        c.setAttribute("r", NODE_RADIUS);
        c.classList.add(id === currentId ? "node-current" : id === compareToId ? "node-compare" : "node-related");
        g.appendChild(c);
        if (selfLabels.has(id)) {
            const { line1, line2 } = selfLabels.get(id);
            const label = document.createElementNS(svg.namespaceURI, "text");
            label.setAttribute("x", x-30);
            label.setAttribute("y", y - NODE_RADIUS - 6-16);
            label.setAttribute("text-anchor", "left");
            label.setAttribute("pointer-events", "none");
            label.classList.add("node-label");

            const tspan1 = document.createElementNS(svg.namespaceURI, "tspan");
            tspan1.setAttribute("x", x-30);
            tspan1.setAttribute("dy", "0");
            tspan1.textContent = line1;

            const tspan2 = document.createElementNS(svg.namespaceURI, "tspan");
            tspan2.setAttribute("x", x-30);
            tspan2.setAttribute("dy", "1.2em");
            tspan2.classList.add("self-label"); // reuse existing italic style for the "by" line
            tspan2.textContent = line2;

            label.appendChild(tspan1);
            label.appendChild(tspan2);
            g.appendChild(label);
        }
        g.style.cursor = "pointer";
        $(g).on("click", () => {
            const url = compareMode
                ? `model_card.html?id=${currentId}&compareto=${id}`
                : `model_card.html?id=${id}`;
            window.location.href = url;
        });
        svg.appendChild(g);
    });

    container.appendChild(svg);
}