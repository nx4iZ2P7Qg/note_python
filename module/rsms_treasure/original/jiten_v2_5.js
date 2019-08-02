/*
発掘大辞典ver1.2をベースにかなり改造してあります。
 - 金額が表示できるように変更。ラジオボタンで金額有り無し選択可能。
 - 発掘スキルをS1-S5の選択式に変更。
 - withはパフォーマンス的にも非推奨らしいのでValueOfMSRandではフル記述、
   OutputHtmlではローカル変数docを使用した略式にしました。
*/

"use strict;"
var RPB = 14.4; //拍あたりの乱数の個数
var ID11 = 0;
const doc = window.top.jiten_r.document;

function TGldChange() {
    ID11 = Math.round(RPB * (parseFloat(document.F1.TGldShousetsu.value) * 4 + parseFloat(document.F1.TGldHaku.value)));
    TChange("Gld");
}

function T11Change() {
    ID11 = parseInt(document.F1.T11ID.value);
    TChange("11");
}

function TPPChange() {
    ID11 = -Math.round(RPB * ((parseFloat(document.F1.TPPShousetsu.value) - 1) * 4 + parseFloat(document.F1.TPPHaku.value) - 1)) + parseInt(document.F1.TPPID.value);
    TChange("PP");
}


function TChange(caller) {
    if (caller != "Gld") {
        var shou = Math.floor(ID11 / (RPB * 4));
        var haku = Math.round(((ID11 / RPB) - shou * 4) * 100) / 100;
        document.F1.TGldShousetsu.value = shou;
        document.F1.TGldHaku.value = haku;
    }
    if (caller != "11") {
        document.F1.T11ID.value = ID11;
    }
    if (caller != "PP") {
        var shou = Math.floor((parseInt(document.F1.TPPID.value) - ID11) / (RPB * 4)) + 1;
        var haku = Math.round((((parseInt(document.F1.TPPID.value) - ID11) / RPB) - (shou - 1) * 4 + 1) * 100) / 100;
        document.F1.TPPShousetsu.value = shou;
        document.F1.TPPHaku.value = haku;
    }
    document.F1.BID.value = ID11 + Math.round(RPB * ((parseInt(document.F1.BShousetsu.value) - 1) * 4 + parseFloat(document.F1.BHaku.value) - 1));
}

function BHakuChange() {
    document.F1.BID.value = ID11 + Math.round(RPB * ((parseInt(document.F1.BShousetsu.value) - 1) * 4 + parseInt(document.F1.BHaku.value) - 1));
}

function BIDChange() {
    var shou = Math.floor((parseInt(document.F1.BID.value) - ID11) / (RPB * 4)) + 1;
    var haku = Math.round((((parseInt(document.F1.BID.value) - ID11) / RPB) - (shou - 1) * 4 + 1) * 100) / 100;
    document.F1.BShousetsu.value = shou;
    document.F1.BHaku.value = haku;
}

function innerChild(innerStrings, parentObj, optKey, optValue) {
    var child = doc.createElement('td');
    child.innerHTML = innerStrings;
    if (optKey) child.setAttribute(optKey, optValue);
    parentObj.appendChild(child);
}

//前回履歴を参照するためのjQueryを利用したLocalStorage実装
function getCondition() {
    //フォームの各パラメータを取得する関数
    var condition = {};
    condition.TGldShousetsu = $('[name="TGldShousetsu"]').val();
    condition.TGldHaku = $('[name="TGldHaku"]').val();
    condition.T11ID = $('[name="T11ID"]').val();
    condition.TPPID = $('[name="TPPID"]').val();
    condition.TPPShousetsu = $('[name="TPPShousetsu"]').val();
    condition.TPPHaku = $('[name="TPPHaku"]').val();
    condition.TR = $('[name="TR"]').val();
    condition.GR = $('[name="GR"]').val();
    condition.ES = $('[name="ES"]').val();
    condition.BShousetsu = $('[name="BShousetsu"]').val();
    condition.BHaku = $('[name="BHaku"]').val();
    condition.BID = $('[name="BID"]').val();
    condition.BKosu = $('[name="BKosu"]').val();
    condition.country = $("#country:checked").val();
    condition.ShowMoney = $('input[name="ShowMoney"]:radio:checked').val();
    return condition;
}

function setCondition(historyHash) {
    //履歴からフォームの各パラメータを設定する関数
    var condition = JSON.parse(historyHash);
    if (condition) {
        $('[name="TGldShousetsu"]').val(condition.TGldShousetsu);
        $('[name="TGldHaku"]').val(condition.TGldHaku);
        $('[name="T11ID"]').val(condition.T11ID);
        $('[name="TPPID"]').val(condition.TPPID);
        $('[name="TPPShousetsu"]').val(condition.TPPShousetsu);
        $('[name="TPPHaku"]').val(condition.TPPHaku);
        $('[name="TR"]').val(condition.TR);
        $('[name="GR"]').val(condition.GR);
        $('[name="ES"]').val(condition.ES);
        $('[name="BShousetsu"]').val(condition.BShousetsu);
        $('[name="BHaku"]').val(condition.BHaku);
        $('[name="BID"]').val(condition.BID);
        $('[name="BKosu"]').val(condition.BKosu);
        $("#country").val([condition.country]);
        $('input[name="ShowMoney"]').val([condition.ShowMoney]);
    }
}

function registerHistory() {
//現在フォームに入力されているパラメータをLocalStorageに書き込み
//checkboxがONならLocalStorageを消去
    var disHistory = $("#discard").prop('checked');
    if (disHistory === false) {
        var condition = getCondition();
        localStorage.setItem('jitenResume', JSON.stringify(condition));
    } else {
        localStorage.clear();
    }
}

function OutputHtml(A_TR, A_GR, ID, N, A_ES, A_SM) {
    var i;
    var j;
    var k;
    var s;
    var bodyObj;
    var tableObj;
    var tbodyObj;

    if (!A_GR) A_GR = "8"; // 默认r8
    if (!A_ES) A_ES = new Array(1, 2, 3, 4, 5); // 默认显示技能lv1-5
    if (!A_SM) A_SM = "full"; // 默认显示full金额

    var HakuOut = new Array(1);//拍出力用・・・1/2拍単位
    var hout = 0;
    var numhout = 0;
    for (i = 0; i < N; i++) {
        if (Math.floor((i + ID - ID11) / (RPB * 0.5)) > Math.floor((i + ID - 1 - ID11) / (RPB * 0.5))) {
            HakuOut[numhout] = i;
            numhout++;
        }
    }

    var ShousetsuOut = new Array(1);//小節出力用
    var sout = 0;
    var numsout = 0;
    for (i = 0; i < N; i++) {
        if (Math.floor((i + ID - ID11) / (RPB * 4)) > Math.floor((i + ID - 1 - ID11) / (RPB * 4))) {
            ShousetsuOut[numsout] = i;
            numsout++;
        }
    }

    doc.open();
    doc.write('<html>\n<head>\n<title>発掘大辞典2</title>\n</head>\n<link rel="stylesheet" href="./css/jiten.css" type="text/css" media="screen" charset="UTF-8">');
    doc.write('<input id="Excel" type="button" value="結果をExcel形式でダウンロード" onclick="Export2Excel()">\n');
    doc.write('<input id="Search" type="button" value="ID検索" onclick="searchID()">\n');
    doc.write("<h2>1小節1拍=ID" + ID11 + "</h2>");
    doc.createTextNode("<h2>1小節1拍=ID" + ID11 + "</h2>");
    doc.write("</html>");


    /*
    var rhtml = doc.createElement('html');
    rhtml.innerHTML = '<link rel="stylesheet" href="./css/jiten.css" type="text/css" media="screen" charset="UTF-8">\n<input id="Excel" type="button" value="結果をExcel形式でダウンロード" onclick="Export2Excel()">';
    doc.appendChild(rhtml);
    var rhead = doc.createElement(head);
    var rtitle = doc.createElement(title);
    rtitle.innerHTML= '発掘大辞典2';
    rhead.appendChild(rtitle);
    rhtml.appendChild(rhead);
    
    var rh2 = doc.createElement(h2);
    rh2.innetHTML='1小節1拍=ID'+ ID11;
    rhtml.appendChild(rh2);
    */


    tableObj = doc.createElement('table');
    tableObj.setAttribute('border', '1');
    tbodyObj = doc.createElement('tbody');
    tbodyObj.setAttribute('id', 'mstbl');
    tbodyObj.setAttribute('class', 'mstbl');

    var trH = doc.createElement('tr');
    var myOpts = ['小節', '拍', 'ID'];
    $.each(myOpts, function () {
        innerChild(this, trH);
    });

    if (A_SM == "none") {
        for (i = 0; i < A_TR.length; i++) {
            for (j = 0; j < A_GR.length; j++) {
                var mainH = "T" + A_TR[i] + "R" + A_GR[j];
                innerChild(mainH, trH);
            }
        }
    } else {
        for (i = 0; i < A_TR.length; i++) {
            for (j = 0; j < A_GR.length; j++) {
                var kingakuH = "T" + A_TR[i] + "金額";
                innerChild(kingakuH, trH, 'align', 'right');
                var mainH = "T" + A_TR[i] + "R" + A_GR[j];
                innerChild(mainH, trH);
            }
        }
    }

    innerChild('サブ候補', trH);
    for (s = 0; s < A_ES.length; s++) {
        var skillH = "スキル" + A_ES[s];
        innerChild(skillH, trH);
    }

    tbodyObj.appendChild(trH);
    tableObj.appendChild(tbodyObj);
    doc.createElement('body');
    bodyObj = doc.getElementsByTagName('body').item(0);
    bodyObj.appendChild(tableObj);
    //workerの生成
    myData = [A_TR, A_GR, ID, N, A_ES, A_SM];
    var NorthAmerica = $("#country").prop('checked');
    if (NorthAmerica === false) {
        var core = "./js/jitenCore.js"
    } else {
        var core = "./js/jitenCore_NA.js"
    }
    var worker = new Worker(core);
    worker.addEventListener('message', function (e) {
        var mstbody = doc.getElementById('mstbl');

        for (i = 0; i < e.data.length; i++) { //列 iのループここから
            var tr = doc.createElement('tr');
            //
            //  小節の出力
            //
            var std = doc.createElement('td'); //小節tdの略。standardではありません。
            std.setAttribute('class', 'SHOUSETSU');
            if (i == ShousetsuOut[sout]) {
                var Shousetsu = Math.floor((i + ID - ID11) / (RPB * 4)) + 1;

                if (sout != numsout - 1) std.rowSpan = ShousetsuOut[sout + 1] - ShousetsuOut[sout];
                else std.rowSpan = N - ShousetsuOut[sout];

                std.innerHTML = Shousetsu;
                std.setAttribute('valign', 'top');
                sout++;
                tr.appendChild(std);
            } else if (i === 0) {
                std.rowSpan = ShousetsuOut[0];
                std.innerHTML = "&nbsp;";
                tr.appendChild(std);
            }

            //
            //  拍の出力
            //
            var htd = doc.createElement('td'); //拍tdの略
            htd.setAttribute('class', 'HAKU');
            if (i == HakuOut[hout]) {
                var HAKU = (Math.floor((i + ID - ID11) / (RPB * 0.5)) / 2 + 1) - Math.floor((i + ID - ID11) / (RPB * 4)) * 4;
                if (hout != numhout - 1) htd.rowSpan = HakuOut[hout + 1] - HakuOut[hout];
                else htd.rowSpan = N - HakuOut[hout];
                htd.innerHTML = HAKU;
                htd.setAttribute('valign', 'top');
                hout++;
                tr.appendChild(htd);
            } else if (i === 0) {
                htd.rowSpan = HakuOut[0];
                htd.innerHTML = "&nbsp;";
                tr.appendChild(htd);
            }
            //
            //  ID,金額,メイン,サブ候補,S1-5をまとめて列に読み込み&書き出し
            //
            var column = e.data[i];
            for (var r = 0; r < column.length; r++) {
                innerChild(column[r], tr)
            }
            mstbody.appendChild(tr);
        } //iのループここまで

        var headObj = doc.getElementsByTagName('head').item(0);
        var srsc = ["jszip", "xlsx", "FileSaver", "jquery-latest.min", "export2xls", "searchID"];
        $.each(srsc, function () {
            var postsrc = doc.createElement("script");
            var srcjs = './js/' + this + '.js';
            postsrc.setAttribute("src", srcjs);
            headObj.appendChild(postsrc);
        });

        doc.close();
        $("#modal", parent.document).remove(); // HTML出力が完了したらmodalを削除
    });

    worker.postMessage(myData);
}

function main() {
    T11Change();

    //jQueryで各変数を定義 
    var A_TR = $('[name="TR"]').val();
    var A_GR = $('[name="GR"]').val();
    var A_ES = $('[name="ES"]').val();
    var A_SM = $('[name="ShowMoney"]:checked').val();
    OutputHtml(A_TR, A_GR, parseInt(document.F1.BID.value), parseInt(document.F1.BKosu.value), A_ES, A_SM);
}




