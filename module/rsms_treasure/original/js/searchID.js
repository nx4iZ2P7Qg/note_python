function searchID() {
    const mrexp = RegExp(/^[1-9][0-9]{2,3}0/);
    const srexp = RegExp(/[GSPWT]{0,3}$/);

    // 入力ダイアログを表示
    userInput = window.prompt("出土した金額,メイン,サブをスペース無しで入力してください。例:4240水鏡WT", "");

    // 入力内容が空なら何もしない
    if (!userInput) return null;

    // 入力内容から金額とサブを抽出
    var sub = userInput.match(srexp)[0];
    if (String(userInput).match(/^[0-9]+/)) {
        var money = String(userInput).match(/^[0-9]+/)[0];
        var mregexp = (String(userInput).match(mrexp) || [])[0] || null;
    }

    // 金額にありえない数値を入力したらはじく
    if ((money) && (money > 20000 || money < 1000 || !mregexp)) {
        alert("正しい金額が入力されていません。");
    } else {
        var str;
        var main;
        // テーブルを検索する文字列を定義。金額+メイン。サブは後で。
        if (mregexp) {
            main = String(userInput).replace(mregexp, "").replace(sub, "");
            str = "(" + mregexp + "|" + mregexp + "\/[1-9][0-9]{2,3}0|[1-9][0-9]{2,3}0\/" + mregexp + ")" + main;
        } else {
            main = String(userInput).replace(sub, "");
            str = main;
        }
        var tr = $('#mstbl').children('tr');

        var found = false;
        $.each(tr, function () {
            // 検索を簡単にするためタグを除去
            var Line = this.innerHTML.replace(/<("[^"]*"|'[^']*'|[^'">])*>/g, '');
            if (Line.match(str)) {
                // 実際のサブ出土候補と照会 
                var subword;
                if (sub.length === 0) subword = '\\+x';
                else subword = '\\+' + sub + '($|\/|,)';
                if (Line.match(subword)) {
                    // パターンマッチした箇所にスクロール 
                    var targetoffset = $(this).offset();
                    $("html,body").animate({scrollTop: targetoffset.top}, {queue: false}, 'fast');
                    found = true;
                    // 最初のパターンマッチが見つかったらそこで終わり
                    return false;
                }
            }
        });
        if (!found) alert("見つかりませんでした。");
    }
}
