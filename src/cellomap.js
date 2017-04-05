// attach itself in certain nodes of the document object

// Note: self-contained! Given the global variable document_data, that
// is, and that should be given in a previous script directly on the
// page.

// Note: x grows down, y grows right, and always have at least one
// cell; allow no data but insist on having a cell; it's not a
// partition anyway when cells can be empty! which they can!

(function () {

    // The document_data object and the view table on the page have
    // the same shape, so that the actual item in document_data can be
    // identified by selecting a label in a cell in a row in the view.

    var view = document.getElementById("view"); // tbody

    // Desired ranges are set outside script. Make sure that lenx and
    // leny are sufficiently non-zero. Actual coordinates are clamped
    // to the desired ranges when assiging items to cells.

    var minx = 0; var maxx = 9; var lenx = maxx - minx;
    var miny = 1; var maxy = 10; var leny = maxy - miny;

    // Been being proposed as Math.clamp already.
    function clamp(x, lo, hi) { return Math.min(Math.max(x, lo), hi); }

    function reflow(data, m, n) { // reflow data in m × n cells
        var it = [];
        for (var r = 0 ; r < m ; ++ r) { // any less cluttered way?
            it.push([]);
            for (var k = 0 ; k < n ; ++ k) {
                it[r].push([]);
            }
        };
        data.forEach(function (row) {
	    row.forEach(function (cell) {
                cell.forEach(function (item) {
		    var stdx = (item[1] - minx) / lenx;
		    var stdy = (item[2] - miny) / leny;
		    var r = clamp(Math.floor(stdx * m), 0, m - 1);
		    var k = clamp(Math.floor(stdy * n), 0, n - 1);
		    // console.log('min-max-len of x', minx, maxx, lenx);
		    // console.log('min-max-len of y', miny, maxy, leny);
		    // console.log('std x, y; r, k', stdx, stdy, r, k);
                    it[r][k].push(item); }) }) });
        return it;
    }

    function reset() { // reset document_data from controls, then
		       // review
	// should also set minx, maxx, lenx, etc. from controls - ok now?
	var midx = +document.getElementById("midx").value;
	var widx = +document.getElementById("widx").value;
	var midy = +document.getElementById("midy").value;
	var widy = +document.getElementById("widy").value;

	minx = midx - widx/2; maxx = midx + widx/2; lenx = maxx - minx;
	miny = midy - widy/2; maxy = midy + widy/2; leny = maxy - miny;

	var m = +document.getElementById("rows").value;
	var n = +document.getElementById("cols").value;
	document_data = reflow(document_data, m, n);
	review(document_data);
    }

    function review(data) { // reset view from data
	// replace table rows with data.length new rows of
	// data[0].length new cells

	var m = data.length;
	var n = data[0].length;

	var newbody = document.createElement("tbody");
	data.forEach(function (row) {
	    var tr = document.createElement("tr");
	    row.forEach(function (cell) {
		var td = document.createElement("td");
		var ul = document.createElement("ul");
		cell.forEach(function (item) {
		    var li = document.createElement("li");
		    li.appendChild(document.createTextNode(item[0]));
		    ul.appendChild(li); });
		ul.onclick = cellHandler(td);
		td.appendChild(ul);
		tr.appendChild(td); });
	    newbody.appendChild(tr); })

	var oldbody = view.getElementsByTagName("tbody")[0];
	view.replaceChild(newbody, oldbody);
    }

    // when an item list is clicked, should be able to find out which
    // actual item was clicked, given the table cell and the event;
    // replace the dl in boxes[0] and swap the boxes[0], boxes[1].
    function cellHandler(cell) { // hm, is that just this.parentNode?
	return function (event) {
	    // alert(cell);
	    // alert(event.target);
	    // alert([cell.parentNode.rowIndex, cell.cellIndex, event.target]);

	    // apparently no way to get the index of the line but loop - what?
	    lines = event.target.parentNode.getElementsByTagName("li");
	    for (var j = 0 ; j < lines.length ; ++ j) {
		if (lines[j] == event.target) {
		    var r = cell.parentNode.rowIndex;
		    var k = cell.cellIndex;
		    var item = document_data[r][k][j];
		    // console.log([r, k, j, item[0], item[1], item[2]]);
		    var newlist = metadatalist(item, r, k);
		    var oldlist = boxes[0].getElementsByTagName("dl")[0];
		    var box = boxes[0]; boxes[0] = boxes[1]; boxes[1] = box;
		    box.replaceChild(newlist, oldlist);
		    break;
		}
	    }
	}
    }

    function metadatalist(item, r, k) { // render item metadata as dl
	var list = document.createElement("dl");
	dataentry(list, item[0], "(" + (r + 1) + ", " + (k + 1) + ")");
	dataentry(list, "(x,y)", "(" + item[1] + ", " + item[2] + ")");
	for (var o in item[3]) {
	    dataentry(list, o, item[3][o]);
	}
	return list;
    }

    function dataentry(list, key, value) { // extend a dl with dt=key, dd=value
	// suppose undefined is obsolete here now that the first key has value
	if (key !== undefined) {
	    var dt = document.createElement("dt");
	    var label = document.createElement("label");
	    label.appendChild(document.createTextNode(key));
	    dt.appendChild(label);
	    list.appendChild(dt);
	}
	if (value !== undefined) {
	    var dd = document.createElement("dd");
	    dd.appendChild(document.createTextNode(value));
	    list.appendChild(dd);
	}
    }

    // these have style="display:none;" until script is allowed to run
    document.getElementById("area").style.display = "";
    document.getElementById("view").style.display = "";

    // showing selected items (but initially showing nothing)
    // Also: how does one make them appear side by side?
    var boxes = [document.createElement("div"), document.createElement("div") ];
    boxes[0].appendChild(document.createElement("dl"));
    boxes[1].appendChild(document.createElement("dl"));
    document.getElementById("meta1").appendChild(boxes[0]);
    document.getElementById("meta2").appendChild(boxes[1]);

    document.getElementById("rows").onchange = reset;
    document.getElementById("cols").onchange = reset;
    document.getElementById("midx").onchange = reset;
    document.getElementById("widx").onchange = reset;
    document.getElementById("midy").onchange = reset;
    document.getElementById("widy").onchange = reset;
    reset();
})();
