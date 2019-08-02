function Export2Excel() {

    function sheet_from_array_of_arrays(data, opts) {
        var ws = {};
        var range = {s: {c: 200, r: 1000000}, e: {c: 0, r: 0}};
        var MaxCulumn = data[0].length;
        var dataString;
        var bgColor;
        var boldBoolean;
        var cell;
        for (var R = 0; R != data.length; ++R) {
            // 列を整形
            if (data[R].length < MaxCulumn) {
                var nullcellnum = MaxCulumn - data[R].length;
                if (nullcellnum == 1) {
                    data[R].unshift('');
                } else if (nullcellnum == 2) {
                    data[R].splice(0, 0, '', '');
                }
            }

            for (var C = 0; C != data[R].length; ++C) {
                if (range.s.r > R) range.s.r = R;
                if (range.s.c > C) range.s.c = C;
                if (range.e.r < R) range.e.r = R;
                if (range.e.c < C) range.e.c = C;

                // classに対応する背景色を静的に記述 
                if (data[R][C].indexOf("class") != "-1") {
                    if ($(data[R][C]).children("div").hasClass('IROTSUKI')) {
                        bgColor = "F781BE";
                    } else if ($(data[R][C]).children("div").hasClass('L3ZEVEN')) {
                        bgColor = "9F81F7";
                    } else if ($(data[R][C]).children("div").hasClass('CHOIRARE')) {
                        bgColor = "A9F5F2";
                    } else if ($(data[R][C]).children("div").hasClass('YUKICHI')) {
                        bgColor = "F9F577";
                    } else {
                        bgColor = "";
                    }
                } else {
                    bgColor = "";
                }

                // 強調表示が含まれるならフォントをboldに
                if (data[R][C].indexOf("strong") != "-1") {
                    dataString = data[R][C].replace(/<("[^"]*"|'[^']*'|[^'">])*>/g, '');
                    boldBoolean = true;
                } else {
                    // 背景がカラーでフォントが通常の場合
                    if (data[R][C].indexOf("class") != "-1") {
                        dataString = data[R][C].replace(/<("[^"]*"|'[^']*'|[^'">])*>/g, '');
                    } else {
                        dataString = data[R][C];
                    }
                    boldBoolean = false;
                }


                if (!bgColor) {
                    cell = {v: dataString, s: {font: {name: "Meiryo", bold: boldBoolean}}};
                } else {
                    cell = {
                        v: dataString,
                        s: {font: {name: "Meiryo", bold: boldBoolean}, fill: {fgColor: {rgb: bgColor}}}
                    };
                }

                if (cell.v == null) continue;
                var cell_ref = XLSX.utils.encode_cell({c: C, r: R});
                cell.t = 's';
                ws[cell_ref] = cell;
            }
        }
        if (range.s.c < 1000000) ws['!ref'] = XLSX.utils.encode_range(range);
        return ws;
    }

    var data = [];
    var data = $('tbl');
    $('tr').each(function (i, tr) {
        var row = [];
        $(tr).children('td').each(function (j, td) {
            var outer = td.outerHTML;
            if (outer.match(/class|strong/)) {
                var o = outer;
            } else {
                var o = td.innerText;
            }
            row.push(o);

        });
        data.push(row);
    });


    function Workbook() {
        if (!(this instanceof Workbook)) return new Workbook();
        this.SheetNames = [];
        this.Sheets = {};
    }

    var key = XLSX.utils.encode_cell({c: 0, r: 0});
    var ws = sheet_from_array_of_arrays(data);

    var workbook = new Workbook();
    workbook.SheetNames.push("result");
    workbook.Sheets["result"] = ws;


    var wbout = XLSX.write(workbook, {
        bookType: 'xlsx',
        bookSST: true,
        type: 'binary'
    });


    function s2ab(s) {
        var buf = new ArrayBuffer(s.length);
        var view = new Uint8Array(buf);
        for (var i = 0; i != s.length; ++i) view[i] = s.charCodeAt(i) & 0xFF;
        return buf;
    }

    saveAs(new Blob([s2ab(wbout)], {type: ""}), "jiten.xlsx");
}



