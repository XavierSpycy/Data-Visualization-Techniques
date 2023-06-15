def stream_graph():
    html_str = """
    <!DOCTYPE html>
    <meta charset="utf-8">

    <body>

    <!-- load the d3.js library -->    	
    <script src="//d3js.org/d3.v7.min.js"></script>
    <script>
    // Get the body's width and height
    var bodyWidth = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
    var bodyHeight = window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;

    // Set the dimensions and margins of the diagram
    var margin = {top: 20, right: 30, bottom: 30, left: 60},
    width = bodyWidth - margin.left - margin.right,
    height = bodyHeight - margin.top - margin.bottom;
    

    d3.csv("critic_score.csv")
        .then(function(data){
            
            // append the svg object to the body of the page
            // appends a 'group' element to 'svg'
            // moves the 'group' element to the top left margin
            var svg = d3.select("body").append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
            .append("g")
                .attr("transform",
                        "translate(" + margin.left + "," + margin.top + ")");
            
            // List of groups = header of the csv files
            var keys = data.columns.slice(1)
            
            //keys = keys.filter(function(d) {return d!='Ashley';})
            //data = data.filter(function(d) {return d.year>=1900 && d.year<=2000;})

            // Add X axis
            var x = d3.scaleLinear()
                .domain(d3.extent(data, function(d) { return d.year; }))
                .range([ 0, width-230]);
            svg.append("g")
                .attr("transform", "translate(0," + height + ")")
                .call(d3.axisBottom(x).ticks(5));

            // Add Y axis
            var y = d3.scaleLinear()
                .domain([-50, 550])
                .range([ height, 0 ]);
            svg.append("g")
                .call(d3.axisLeft(y));

            // color palette
            var color = d3.scaleOrdinal()
                .domain(keys)
                .range(['#e41a1c','#377eb8','#4daf4a','#984ea3','#ff7f00','#ffff33','#a65628','#f781bf',
                '#8dd3c7','#bebada','#fb8072','#80b1d3','#fdb462','#b3de69','#fccde5','#bc80bd'])

            //stack the data?
            var stackedData = d3.stack()
                .offset(d3.stackOffsetWiggle)
                .keys(keys)
                (data)
            

            // Show the areas
            svg
                .selectAll("mylayers")
                .data(stackedData)
                .enter()
                .append("path")
                .style("fill", function(d) { return color(d.key); })
                .attr("d", d3.area()
                    .x(function(d, i) { return x(d.data.year); })
                    .y0(function(d) { return y(d[0]); })
                    .y1(function(d) { return y(d[1]); })
                )
            .append("title")
                .text(function(d) { return d.key;});

            // set the dimensions and margins of the legend
            var legendWidth = 100;
            var legendHeight = keys.length * 20;

            // append a group for the legend
            var legend = svg.append("g")
                .attr("transform", "translate(" + (width - 230 + margin.right / 2) + ",0)");


            // add rectangles for the legend
            legend.selectAll("rect")
                .data(keys)
                .enter()
                .append("rect")
                .attr("x", 0)
                .attr("y", function(d, i) { return i * 20; })
                .attr("width", 10)
                .attr("height", 10)
                .style("fill", function(d) { return color(d); });

            // add labels for the legend
            legend.selectAll("text")
                .data(keys)
                .enter()
                .append("text")
                .attr("x", 15)
                .attr("y", function(d, i) { return i * 20 + 9; })
                .text(function(d) { return d; });

            });
            </script>
            </body>
    """
    with open("stream_graph.html", "w") as f:
        f.write(html_str)

def small_multiples():
    html_str = """
    <!DOCTYPE html>
    <meta charset="utf-8">
    <body>

    <!-- load the d3.js library -->    	
    <script src="//d3js.org/d3.v7.min.js"></script>

    <!-- Create a div where the graph will take place -->
    <div id="my_dataviz"></div>
    <script>

    // Dimension of the whole chart. Only one size since it has to be square
    var marginWhole = {top: 10, right: 10, bottom: 10, left: 10},
        sizeWhole = 1280 - marginWhole.left - marginWhole.right

    // Create the svg area
    var svg = d3.select("#my_dataviz")
    .append("svg")
        .attr("width", sizeWhole  + marginWhole.left + marginWhole.right + 150)
        .attr("height", sizeWhole  + marginWhole.top + marginWhole.bottom)
    .append("g")
        .attr("transform", "translate(" + marginWhole.left + "," + marginWhole.top + ")");

    d3.csv("high_dimensional.csv").then(function(data) {
        
    // What are the numeric variables in this dataset? How many do I have
    var allVar = data.columns.filter(function(d) {return d!='Genre'})
    var numVar = allVar.length

    // Now I can compute the size of a single chart
    mar = 20
    size = sizeWhole / numVar


    // ----------------- //
    // Scales
    // ----------------- //

    // Create a scale: gives the position of each pair each variable
    var position = d3.scalePoint()
        .domain(allVar)
        .range([0, sizeWhole-size])

    // Color scale: give me a species name, I return a color
    var color = d3.scaleOrdinal()
    var color = d3.scaleOrdinal()
        .domain(['Sports', 'Racing', 'Platform', 'Misc', 'Action', 'Shooter', 'Fighting', 'Simulation', 'Role-Playing', 'Adventure', 'Puzzle', 'Strategy'])
        .range([ "#402D54", "#D18975", "#8FD175", "#375E97", "#FB6542", "#FFBB00", "#3F681C", "#f37736", "#046865", "#2F6690", "#839788", "#BCA136"]);

    // ------------------------------- //
    // Add charts
    // ------------------------------- //
    for (i in allVar){
        for (j in allVar){

        // Get current variable name
        var var1 = allVar[i]
        var var2 = allVar[j]

        // If var1 == var2 I'm on the diagonal, I skip that
        if (var1 === var2) { continue; }

        // Add X Scale of each graph
        xextent = d3.extent(data, function(d) { return +d[var1] })
        var x = d3.scaleLinear()
            .domain(xextent).nice()
            .range([ 0, size-2*mar ]);

        // Add Y Scale of each graph
        yextent = d3.extent(data, function(d) { return +d[var2] })
        var y = d3.scaleLinear()
            .domain(yextent).nice()
            .range([ size-2*mar, 0 ]);

        // Add a 'g' at the right position
        var tmp = svg
            .append('g')
            .attr("transform", "translate(" + (position(var1)+mar) + "," + (position(var2)+mar) + ")");

        // Add X and Y axis in tmp
        tmp.append("g")
            .attr("transform", "translate(" + 0 + "," + (size-mar*2) + ")")
            .call(d3.axisBottom(x).ticks(3));
        tmp.append("g")
            .call(d3.axisLeft(y).ticks(3));

        // Add circle
        tmp
            .selectAll("myCircles")
            .data(data)
            .enter()
            .append("circle")
            .attr("cx", function(d){ return x(+d[var1]) })
            .attr("cy", function(d){ return y(+d[var2]) })
            .attr("r", 3)
            .attr("fill", function(d){ return color(d.Genre)})
        }
    }


    // ------------------------------- //
    // Add variable names = diagonal
    // ------------------------------- //
    for (i in allVar){
        for (j in allVar){
        // If var1 == var2 i'm on the diagonal, otherwisee I skip
        if (i != j) { continue; }
        // Add text
        var var1 = allVar[i]
        var var2 = allVar[j]
        svg
            .append('g')
            .attr("transform", "translate(" + position(var1) + "," + position(var2) + ")")
            .append('text')
            .attr("x", size/2)
            .attr("y", size/2)
            .text(var1)
            .attr("text-anchor", "middle")

        }
    }
    var legend = svg.selectAll(".legend")
        .data(color.domain())
        .enter().append("g")
        .attr("class", "legend")
        .attr("transform", function(d, i) { return "translate(150," + i * 20 + ")"; });
        
    // Add colored squares to the legend
    legend.append("rect")
        .attr("x", sizeWhole - 18)
        .attr("width", 18)
        .attr("height", 18)
        .style("fill", color);

    // Add text to the legend
    legend.append("text")
        .attr("x", sizeWhole - 24)
        .attr("y", 9)
        .attr("dy", ".35em")
        .style("text-anchor", "end")
        .text(function(d) { return d; });

    })

    </script>
    </body>
    """
    with open("small_multiples.html", "w") as f:
        f.write(html_str)


def tree_radial():
    html_str = """
    <!DOCTYPE html>
    <meta charset="utf-8">
    <style> /* set the CSS */

    h1 {
    text-align: center;
    }
    .node circle {
    stroke: steelblue;
    stroke-width: 3px;
    }

    .node text { font: 5px sans-serif; }

    .node--internal text {
    text-shadow: 0 1px 0 #fff, 0 -1px 0 #fff, 1px 0 0 #fff, -1px 0 0 #fff;
    }

    .link {
    fill: none;
    stroke: #ccc;
    stroke-width: 2px;
    }

    </style>

    <body>
    <!-- load the d3.js library -->    	
    <script src="//d3js.org/d3.v7.min.js"></script>
    <script>

    // set the dimensions and margins of the diagram
    var margin = {top: 10, right: 150, bottom: 30, left: 90},
        width = 1200 + margin.bottom + margin.top,
        height = 1500;

    var link, node;

    // declares a tree layout and assigns the size
    var scaleFactor = 0.8;
    var treemap = d3.tree()
        .size([2 * Math.PI, width/2 * scaleFactor])
        .separation((a, b) => (a.parent == b.parent ? 1 : 2) / a.depth);

    // Add this function to generate random colors
    function getRandomColor() {
    var letters = "0123456789ABCDEF";
    var color = "#";
    for (var i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
    }
    // loads tree data
    d3.json("tree_dataset.json")
        .then(function(treeData){
        //  assigns the data to a hierarchy using parent-child relationships
        var nodes = d3.hierarchy(treeData, function(d) {
            return d.children;
        })
        .sum(function(d) { return d.size ? d.size : 1; })
        .eachBefore(node => {
        if (node.depth === 0) {
            node.color = "#808080";
            node.r = 10;
        } else if (node.depth === 1) {
            node.color = getRandomColor();
        } else {
        node.color = node.parent.color;
        }
        });

        // maps the node data to the tree layout
        nodes = treemap(nodes);

        // append the svg object to the body of the page
        // appends a 'group' element to 'svg'
        // moves the 'group' element to the top left margin
        var svg = d3.select("body").append("svg")
            .attr("width", width + margin.left + margin.right)
            .attr("height", height + margin.top + margin.bottom),
            g = svg.append("g")
            .attr("transform",
                    "translate(" + (margin.left + width/2) + "," + (height/2 - margin.bottom - margin.top) + ")");

        // adds the links between the nodes
        link = g.selectAll(".link")
            .data( nodes.links())
        .enter().append("path")
            .attr("class", "link")
            .attr("d", d3.linkRadial()
            .angle(d => d.x)
            .radius(d => d.y));


        // adds each node as a group
        node = g.selectAll(".node")
            .data(nodes.descendants())
        .enter().append("g")
            .attr("transform", d => `
            rotate(${d.x * 180 / Math.PI - 90})
            translate(${d.y},0)
        `);
        
        // adds the circle to the node
        node.append("circle")
        .attr("r", d => d.r ? d.r : Math.sqrt(d.value ? d.value : 1) * 1.5)
        .style("fill", function(d) {
        return d.color;
    })
    .style("stroke", function(d) {
        return d.color;
    });

        // adds the text to the node
        node.append("text")
        .attr("dy", "0.31em")
        .attr("font-size", "8px")
        .attr("x", d => d.x < Math.PI === !d.children ? 6 : -6)
        .attr("text-anchor", d => d.x < Math.PI === !d.children ? "start" : "end")
        .attr("transform", d => d.x >= Math.PI ? "rotate(180)" : null)
        .text(d => d.data.name)
        .clone(true).lower()
        .attr("stroke", "white");

    });
        
    </script>
    </body>
    """
    with open("tree_radial.html", "w") as f:
        f.write(html_str)