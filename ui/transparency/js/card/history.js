function renderHistoryGraph(history, currentId, container) {
    if (!history || history.length === 0) return;
    if (history.length<2) return;
    const nodeIds = new Set();
    history.forEach(([u, v]) => {
        nodeIds.add(u);
        nodeIds.add(v);
    });

    const rootId = Math.min(...nodeIds);
    const X_SPACING = 120;
    const Y_SPACING = 30;
    const NODE_RADIUS = 10;
    const adj = new Map();
    const edges = [];
    const selfLabels = new Map();
    history.forEach(([u, v, msg]) => {
        if (u === v) {
            if (msg) selfLabels.set(u, msg);
            return;
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

    const ys = Array.from(yPos.values());
    const minY = Math.min(...ys);
    yPos.forEach((v, k) => yPos.set(k, v - minY + 40));

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
        const y = yPos.get(id);
        const g = document.createElementNS(svg.namespaceURI, "g");
        g.classList.add("node");
        const c = document.createElementNS(svg.namespaceURI, "circle");
        c.setAttribute("cx", x);
        c.setAttribute("cy", y);
        c.setAttribute("r", NODE_RADIUS);
        c.classList.add(id === currentId ? "node-current" : "node-related");
        g.appendChild(c);
        if (selfLabels.has(id)) {
            const label = document.createElementNS(svg.namespaceURI, "text");
            label.setAttribute("x", x);
            label.setAttribute("y", y - NODE_RADIUS - 6);
            label.setAttribute("text-anchor", "middle");
            label.setAttribute("pointer-events", "none");
            label.classList.add("node-label");
            label.textContent = selfLabels.get(id);
            g.appendChild(label);
        }
        g.style.cursor = "pointer";
        g.addEventListener("click", () => {
            window.location.href = `model_card.html?id=${id}`;
        });
        svg.appendChild(g);
    });

    container.appendChild(svg);
}