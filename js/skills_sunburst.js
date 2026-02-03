// D3 Interactive Sunburst Visualization
function renderSunburst(dataSource, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;

    d3.select("#" + containerId).selectAll("*").remove();

    const width = 900;
    const height = 900;
    const radius = width / 6;

    const svg = d3.select("#" + containerId)
        .append("svg")
        .attr("viewBox", `0 0 ${width} ${height}`)
        .style("max-width", "100%")
        .style("height", "auto")
        .style("font-family", "Inter, sans-serif")
        .style("overflow", "visible");

    // -- Master Container Group (Enables Zoom/Pan) --
    const masterGroup = svg.append("g").attr("class", "master-container");

    // -- Rotation Group (Enables Spinning) --
    const rotationGroup = masterGroup.append("g")
        .attr("class", "rotation-container")
        .attr("transform", `translate(${width / 2},${width / 2})`);

    const g = rotationGroup.append("g");

    let currentRotation = 0;

    // -- Zoom Logic --
    const zoom = d3.zoom()
        .scaleExtent([0.5, 4])
        .on("zoom", (event) => {
            masterGroup.attr("transform", event.transform);
        });

    svg.call(zoom)
        .on("dblclick.zoom", null);

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

    const tooltip = d3.select("#sunburst-tooltip");

    const dataPromise = typeof dataSource === 'string'
        ? fetch(dataSource).then(r => r.json())
        : Promise.resolve(dataSource);

    dataPromise.then(data => {
        // ... (data processing same as before)
        const rootData = { name: "Waal Bridge", children: [] };

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

        const root = d3.hierarchy(rootData)
            .sum(d => (d.children ? 0 : 1));

        const partition = d3.partition()
            .size([2 * Math.PI, root.height + 1]);

        partition(root);

        const arc = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
            .padRadius(radius * 1.5)
            .innerRadius(d => d.y0 * radius)
            .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));

        const arcTransition = d3.arc()
            .startAngle(d => d.x0)
            .endAngle(d => d.x1)
            .padAngle(d => Math.min((d.x1 - d.x0) / 2, 0.005))
            .padRadius(radius * 1.5)
            .innerRadius(d => d.y0 * radius)
            .outerRadius(d => Math.max(d.y0 * radius, d.y1 * radius - 1));

        const brandColors = ["#38bdf8", "#818cf8", "#c084fc", "#fb7185", "#34d399"];

        const path = g.append("g")
            .selectAll("path")
            .data(root.descendants().slice(1))
            .join("path")
            .attr("fill", d => {
                while (d.depth > 1) d = d.parent;
                const index = root.children.indexOf(d);
                return brandColors[index % brandColors.length];
            })
            .attr("fill-opacity", d => d.children ? 0.8 : 0.6)
            .attr("pointer-events", "auto")
            .attr("d", arc)
            .style("cursor", "pointer")
            .style("transition", "fill-opacity 0.3s ease");

        path.append("title")
            .text(d => `${d.ancestors().map(d => d.data.name).reverse().join("/")}\n${d3.format(",d")(d.value)}`);

        const label = g.append("g")
            .attr("pointer-events", "none")
            .attr("text-anchor", "middle")
            .style("user-select", "none")
            .selectAll("text")
            .data(root.descendants().slice(1))
            .join("text")
            .attr("dy", "0.35em")
            .attr("fill", "white")
            .style("font-size", "10px")
            .style("font-weight", "600")
            .attr("fill-opacity", d => +labelVisible(d))
            .attr("transform", d => labelTransform(d))
            .text(d => d.data.name);

        const centerText = g.append("text")
            .attr("text-anchor", "middle")
            .attr("dy", "0.35em")
            .style("font-size", "14px")
            .style("font-weight", "bold")
            .style("fill", "#38bdf8")
            .text("Waal Bridge");

        const parent = g.append("circle")
            .datum(root)
            .attr("r", radius)
            .attr("fill", "none")
            .attr("pointer-events", "all")
            .on("click", (event, p) => clicked(event, p));

        function clicked(event, p) {
            centerText.text(p.depth === 0 ? "Waal Bridge" : p.data.name);
            parent.datum(p.parent || root);

            root.each(d => d.target = {
                x0: Math.max(0, Math.min(1, (d.x0 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
                x1: Math.max(0, Math.min(1, (d.x1 - p.x0) / (p.x1 - p.x0))) * 2 * Math.PI,
                y0: Math.max(0, d.y0 - p.depth),
                y1: Math.max(0, d.y1 - p.depth)
            });

            const t = g.transition().duration(750);

            path.transition(t)
                .tween("data", d => {
                    const i = d3.interpolate(d.current, d.target);
                    return t => d.current = i(t);
                })
                .filter(function (d) {
                    return +this.getAttribute("fill-opacity") || arcVisible(d.target);
                })
                .attr("fill-opacity", d => arcVisible(d.target) ? (d.children ? 0.8 : 0.6) : 0)
                .attr("pointer-events", d => arcVisible(d.target) ? "auto" : "none")
                .attrTween("d", d => () => arcTransition(d.current));

            label.filter(function (d) {
                return +this.getAttribute("fill-opacity") || labelVisible(d.target);
            }).transition(t)
                .attr("fill-opacity", d => +labelVisible(d.target))
                .attrTween("transform", d => () => labelTransform(d.current));
        }

        path.on("mouseover", function (event, d) {
            d3.select(this).attr("fill-opacity", 1);
            tooltip.style("opacity", 1)
                .html(`<div class="font-mono text-sky-400">> ${d.data.name}</div><div class="text-xs text-gray-400 mt-1">${d.data.details || 'System Node'}</div>`)
                .style("left", (event.pageX + 10) + "px")
                .style("top", (event.pageY - 28) + "px");
        })
            .on("mouseout", function (event, d) {
                d3.select(this).attr("fill-opacity", d.children ? 0.8 : 0.6);
                tooltip.style("opacity", 0);
            })
            .on("click", (event, p) => clicked(event, p));

        function arcVisible(d) {
            return d.y1 <= 6 && d.y0 >= 1 && d.x1 > d.x0;
        }

        function labelVisible(d) {
            return d.y1 <= 6 && d.y0 >= 1 && (d.y1 - d.y0) * (d.x1 - d.x0) > 0.03;
        }

        function labelTransform(d) {
            // Absolute angle = segment angle + current chart rotation
            const x_rad = (d.x0 + d.x1) / 2;
            const x_deg = x_rad * 180 / Math.PI;

            // Factor in global rotation to determine absolute visual orientation
            const absolute_deg = (x_deg + currentRotation) % 360;
            const normalized_abs = absolute_deg < 0 ? absolute_deg + 360 : absolute_deg;

            const y = (d.y0 + d.y1) / 2 * radius;

            // Flip if in the left half of the visual circle (180 to 360 deg) to keep text upright
            const flip = (normalized_abs > 180 && normalized_abs < 360) ? 180 : 0;

            return `rotate(${x_deg - 90}) translate(${y},0) rotate(${flip})`;
        }

        root.each(d => d.current = d);

        // -- Spin Controls (Inside Data Handler) --
        function updateRotation(animate = true) {
            const t = animate ? rotationGroup.transition().duration(500).ease(d3.easeCubicOut) : rotationGroup;
            t.attr("transform", `translate(${width / 2},${width / 2}) rotate(${currentRotation})`);

            // Update labels to remain upright
            label.transition(animate ? d3.transition().duration(500) : null)
                .attr("transform", d => labelTransform(d.current || d));

            // Counter-rotate center hub to keep it level
            centerText.transition(animate ? d3.transition().duration(500) : null)
                .attr("transform", `rotate(${-currentRotation})`);
        }

        d3.select("#spin-left").on("click", () => {
            currentRotation -= 30;
            updateRotation();
        });

        d3.select("#spin-right").on("click", () => {
            currentRotation += 30;
            updateRotation();
        });

        d3.select("#spin-reset").on("click", () => {
            currentRotation = 0;
            updateRotation();
        });
    });
}
