// D3 Radar "Orbit" Visualization
function renderRadar(dataSource, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    // Remove any previous SVG (re-use container)
    d3.select("#" + containerId).selectAll("*").remove();

    const width = 900;
    const height = 900;
    const padding = 100;
    // Radial tree needs slightly less radius to fitting labels
    const radius = width / 2 - padding;

    const svg = d3.select("#" + containerId)
        .append("svg")
        .attr("viewBox", `-${width / 2} -${height / 2} ${width} ${height}`)
        .style("max-width", "100%")
        .style("height", "auto")
        .style("font-family", "'Courier New', Courier, monospace") // Radar Font
        .style("overflow", "visible");

    // -- Master Container Group (Fixes "move differently" zoom bug) --
    const masterGroup = svg.append("g").attr("class", "master-container");

    // -- Zoom Logic --
    const zoom = d3.zoom()
        .scaleExtent([0.5, 4]) // Min 0.5x, Max 4x
        .on("zoom", (event) => {
            masterGroup.attr("transform", event.transform);
        });

    svg.call(zoom)
        .on("dblclick.zoom", null); // Disable double click zoom

    // Bind Controls
    d3.select("#zoom-in").on("click", () => {
        svg.transition().duration(300).call(zoom.scaleBy, 1.2);
    });

    d3.select("#zoom-out").on("click", () => {
        svg.transition().duration(300).call(zoom.scaleBy, 0.8);
    });

    d3.select("#zoom-reset").on("click", () => {
        svg.transition().duration(500).call(zoom.transform, d3.zoomIdentity);
    });

    // -- Radar Grid Aesthetics --

    // Gradient for the sweep
    const defs = svg.append("defs");
    const sweepGradient = defs.append("radialGradient")
        .attr("id", "sweepGradient")
        .attr("cx", "50%")
        .attr("cy", "50%")
        .attr("r", "50%");

    sweepGradient.append("stop").attr("offset", "0%").attr("stop-color", "rgba(56, 189, 248, 0)");
    sweepGradient.append("stop").attr("offset", "80%").attr("stop-color", "rgba(56, 189, 248, 0.05)");
    sweepGradient.append("stop").attr("offset", "100%").attr("stop-color", "rgba(56, 189, 248, 0.2)"); // Lighter sweep

    // Concentric Circles (Radar Grid)
    const gridGroup = masterGroup.append("g").attr("class", "grid-group");
    const ticks = [0.2, 0.4, 0.6, 0.8, 1.0];

    ticks.forEach(t => {
        gridGroup.append("circle")
            .attr("r", radius * t)
            .attr("fill", "none")
            .attr("stroke", "#38bdf8") // Sky 400
            .attr("stroke-width", 1)
            .attr("stroke-opacity", 0.15)
            .style("filter", "drop-shadow(0 0 2px #38bdf8)");
    });

    // Crosshairs
    gridGroup.append("line")
        .attr("x1", -radius).attr("y1", 0).attr("x2", radius).attr("y2", 0)
        .attr("stroke", "#38bdf8").attr("stroke-width", 1).attr("stroke-opacity", 0.1);
    gridGroup.append("line")
        .attr("x1", 0).attr("y1", -radius).attr("x2", 0).attr("y2", radius)
        .attr("stroke", "#38bdf8").attr("stroke-width", 1).attr("stroke-opacity", 0.1);

    // Scanner Sweep Animation
    const sweep = gridGroup.append("path")
        .attr("d", d3.arc()({
            innerRadius: 0,
            outerRadius: radius,
            startAngle: 0,
            endAngle: Math.PI / 4 // 45 degree sector
        }))
        .attr("fill", "url(#sweepGradient)")
        .style("mix-blend-mode", "screen"); // Screen for dark bg

    d3.timer((elapsed) => {
        const angle = (elapsed / 3000) * 360; // 3 seconds per rotation
        sweep.attr("transform", `rotate(${angle})`);
    });

    // -- Data Logic --

    const tooltip = d3.select("#sunburst-tooltip");

    const dataPromise = typeof dataSource === 'string'
        ? fetch(dataSource).then(response => {
            if (!response.ok) throw new Error("File not found");
            return response.json();
        })
        : Promise.resolve(dataSource);

    dataPromise.then(data => {
        const rootData = { name: "Waal Bridge", children: [] };

        // Helper to flatten
        function processChildren(obj) {
            if (obj.children) {
                return Object.entries(obj.children).map(([k, v]) => ({
                    name: k,
                    ...v,
                    children: processChildren(v)
                }));
            } else {
                const kids = [];
                for (const [k, v] of Object.entries(obj)) {
                    if (k !== 'id' && k !== 'name' && k !== 'details') {
                        kids.push({
                            name: k,
                            ...v,
                            children: processChildren(v)
                        });
                    }
                }
                return kids.length > 0 ? kids : null;
            }
        }

        rootData.children = Object.entries(data).map(([key, value]) => ({
            name: key,
            ...value,
            children: processChildren(value)
        }));

        // Hierarchy & Layout
        const root = d3.hierarchy(rootData);

        // Cluster layout with increased separation for overlap prevention
        const treeLayout = d3.cluster()
            .size([2 * Math.PI, radius - 60]) // Reduce radius slightly to give text room
            .separation((a, b) => (a.parent == b.parent ? 1.5 : 3) / a.depth); // Increased separation

        treeLayout(root);

        // Nodes (Points)
        // Draw links individually to control "Spoke" style
        const linkGroup = masterGroup.append("g").attr("class", "links");

        // Custom straight line generator for "spokes"
        const radialLine = d3.line()
            .x(d => d.y * Math.cos(d.x - Math.PI / 2))
            .y(d => d.y * Math.sin(d.x - Math.PI / 2));

        linkGroup.selectAll("path")
            .data(root.links())
            .join("path")
            .attr("d", d => {
                const sourceAngle = d.source.x - Math.PI / 2;
                const targetAngle = d.target.x - Math.PI / 2;

                const sx = d.source.y * Math.cos(sourceAngle);
                const sy = d.source.y * Math.sin(sourceAngle);
                const tx = d.target.y * Math.cos(targetAngle);
                const ty = d.target.y * Math.sin(targetAngle);

                return `M${sx},${sy}L${tx},${ty}`;
            })
            .attr("fill", "none")
            .attr("stroke", d => d.source.depth === 0 ? "#38bdf8" : "#818cf8") // Sky 400, Indigo 400
            .attr("stroke-width", d => d.source.depth === 0 ? 2 : 1) // Thicker main spokes
            .attr("stroke-opacity", 0.3);

        // Nodes (Points)
        const nodeGroup = masterGroup.append("g");

        const nodes = nodeGroup.selectAll("circle")
            .data(root.descendants())
            .join("circle")
            .attr("transform", d => `
                    rotate(${d.x * 180 / Math.PI - 90})
                    translate(${d.y},0)
                `)
            .attr("r", d => d.depth === 0 ? 12 : (d.children ? 6 : 4)) // Bigger hub
            .attr("fill", d => d.depth === 0 ? "#0f172a" : (d.children ? "#38bdf8" : "#818cf8"))
            .attr("stroke", d => d.depth === 0 ? "#38bdf8" : "#fff")
            .attr("stroke-width", d => d.depth === 0 ? 3 : 1) // Hub ring
            .style("filter", "drop-shadow(0 0 5px #38bdf8)") // Brand blue glow
            .style("cursor", "pointer");

        // Labels with Wrapping Logic
        const labels = nodeGroup.append("g")
            .selectAll("text")
            .data(root.descendants())
            .join("text")
            .attr("transform", d => `
                    rotate(${d.x * 180 / Math.PI - 90}) 
                    translate(${d.y},0) 
                    rotate(${d.x >= Math.PI ? 180 : 0})
                `)
            .attr("dy", d => d.depth === 0 ? "2.5em" : "0.31em") // Push root label below the circle
            .attr("x", d => d.depth === 0 ? 0 : (d.x < Math.PI === !d.children ? 8 : -8))
            .attr("text-anchor", d => d.depth === 0 ? "middle" : (d.x < Math.PI === !d.children ? "start" : "end"))
            .style("fill", d => d.depth === 0 ? "#38bdf8" : "#ffffff") // Sky 400 hub, Pure White text
            .style("font-size", d => d.depth === 0 ? "16px" : "11px") // Slightly larger font
            .style("font-weight", d => d.depth === 0 ? "bold" : "600") // Semi-bold for precision
            .style("letter-spacing", d => d.depth === 0 ? "2px" : "0.5px")
            .style("pointer-events", "none")
            .each(function (d) {
                const text = d.data.name;
                const el = d3.select(this);
                const limit = 16;

                if (text.length > limit && d.depth > 0) {
                    const words = text.split(/\s+/).reverse(); // Split by space

                    let lines = [];

                    if (words.length === 1 && text.length > limit) {
                        lines.push(text);
                    } else {
                        const originalWords = text.split(/\s+/);
                        let currentLine = [];

                        originalWords.forEach(word => {
                            if ((currentLine.join(" ").length + word.length) > limit) {
                                lines.push(currentLine.join(" "));
                                currentLine = [word];
                            } else {
                                currentLine.push(word);
                            }
                        });
                        if (currentLine.length > 0) lines.push(currentLine.join(" "));
                    }

                    // Render tspan
                    el.text("");
                    lines.forEach((l, i) => {
                        el.append("tspan")
                            .attr("x", d.x < Math.PI === !d.children ? 8 : -8)
                            .attr("dy", i === 0 ? (lines.length > 1 ? "-0.3em" : "0.31em") : "1.1em")
                            .style("fill", "#ffffff")
                            .text(l);
                    });
                } else {
                    el.text(text);
                }
            });

        // Interaction
        nodes.on("mouseover", function (event, d) {
            d3.select(this).attr("r", 8).style("fill", "#fff");

            tooltip.style("opacity", 1)
                .html(`<div class="font-mono text-sky-400">> ${d.data.name}</div><div class="text-xs text-gray-400 mt-1">${d.data.details || 'System Node'}</div>`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 28) + "px");
        })
            .on("mouseout", function (event, d) {
                d3.select(this).attr("r", d.depth === 0 ? 8 : (d.children ? 4 : 3)).style("fill", d.children ? "#38bdf8" : "#818cf8");
                tooltip.style("opacity", 0);
            });

    })
        .catch(err => {
            console.error(err);
            container.innerHTML = "<div class='text-red-500 font-mono'>SYSTEM ERROR: DATA CORRUPT</div>";
        });
}
