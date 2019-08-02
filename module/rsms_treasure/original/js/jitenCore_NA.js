/*
 マルチスレッド対応のため分離
  乱数、金額、メイン、サブアイテムまでを生成して配列に格納、呼び出し元に渡す
*/

"use strict;"

const Stable = "GSSPPPWWTT";//サブアイテムのテーブル、"安定(stable)"ではありません。

const Ztable = new Array(
    ["雪", "雪", "雪", "竜剣", "雪"],
    ["炎", "ベルジュ", "ランギ", "青の剣", "紅孔雀"],
    ["PD", "ブリム", "AJ", "レディ", "竜ケレ"],
    ["AM", "魔石", "刀", "ヴォパ", "竜マリ"],
    ["LL", "光", "藤", "竜盾", "水鏡"],
    ["銀", "魔骨", "黒鎧", "竜鎧", "月下美人"]
);//財宝メインテーブル

function ValueOfMSRand(n) {
    var i;
    if (n > this.ID) {
        while (n - this.ID > 100) {
            this.X = (this.X * this.A100 + this.B100) % (1 << 24);
            this.ID += 100;
        }
        while (n != this.ID) {
            this.X = (this.X * this.A1 + this.B1) % (1 << 24);
            this.ID++;
        }
    } else {
        while (this.ID - n > 100) {
            this.X = (this.X * this.A100_b + this.B100_b) % (1 << 24);
            this.ID -= 100;
        }
        while (n != this.ID) {
            this.X = (this.X * this.A1_b + this.B1_b) % (1 << 24);
            this.ID--;
        }
    }
    return this.X;
}

function MSRand() {
    this.ID = 0;
    this.X = 3830989;

    this.A1 = 12996205;
    this.B1 = 123453;
    this.A1_b = 12184421;
    this.B1_b = 8306415;

    this.A100 = 13620369;
    this.B100 = 7897084;
    this.A100_b = 3566705;
    this.B100_b = 11088324;

    this.Value = ValueOfMSRand;
}

//workerここから
self.addEventListener('message', function (e) {
    var i;
    var j;
    var k;
    var s;
    var A_TR = e.data[0];
    var A_GR = e.data[1];
    var ID = e.data[2];
    var N = e.data[3];
    var A_ES = e.data[4];
    var A_SM = e.data[5];
    //このworkerが呼び出し元に渡すオブジェクトを定義:行列ZdataTable
    var ZdataTable = [];
    //列 : ID 金額 メイン サブ候補 スキルごとの出土サブ
    //行 : 列がID個数分並ぶ
    //行列に格納されるのはStringで、渡し先で楽をするためhtmlの整形までやる

    if (!A_ES) {
        A_ES = new Array(1, 2, 3, 4, 5);
    }
    if (!A_SM) {
        A_SM = "full";
    }

    var R = new MSRand();
    ran = new Array(N + 40);
    for (i = 0; i < N + 40; i++) {
        ran[i] = R.Value(ID - 90 + i);
    }

    for (i = 0; i < N; i++) {
        var Lv;//財宝のレベル
        var Zk;//財宝の族
        var X;
        var sub = new Array(3);//サブアイテムの候補3つ
        j = i + 20
        //財宝カラムの定義
        var Zcolumn = [];
        var idHTML = ID + i;
        Zcolumn.push(idHTML);// IDをcolumnにpush
        Zk = ran[j] % 6; //族は乱数を6で割った余り。
        for (t = 0; t < A_TR.length; t++) {
            var TR = Number(A_TR[t]);

            //金額ここから
            if (A_SM != "none") {
                var Zkingaku = (Math.floor((ran[j - 5] % (TR + 2) + ran[j - 4] % (TR + 2)) / 2) * 10 + 50 * TR + 100) * 10;
                moneyHTML = "<div align=right>" + Zkingaku + "</div>";
            } //金額ここまで

            // メインここから
            for (g = 0; g < A_GR.length; g++) {
                var GR = Number(A_GR[g]);
                X = (ran[j - 2] % (GR + 1)) + (ran[j - 1] % (TR + 1));
                //乱数を(バトルランク+1)で割った余り＋別の乱数を(テーブルランク+1)で割った余り
                //この値は0～（バトルランク＋テーブルランク）
                //Lv=ran[j-1]%((X-X%4)/4 +1);// レベルの最大値は X/4 (余りが切り捨てられる)
                Lv = (X - X % 4) / 4; //北米版はこう
                var color = "";
                if (Lv > 2) {//まず、Lv3とLv4を処理
                    if (Lv == 4 || Zk % 2 == 1) {//Lv4 ＆ 奇数族Lv3（青、ヴォパ、竜鎧）
                        if (Zk !== 0) { //雪は除く
                            color = "IROTSUKI";
                        }
                    } else {
                        color = "L3ZEVEN";
                    }
                } else if (Lv == 2 || (Lv == 1 && Zk % 2 == 1)) {//Lv2と奇数族Lv1を処理
                    if (Zk !== 0) {//やっぱり雪は除く
                        color = "CHOIRARE";
                    }
                }
                var mainHTML;
                //背景色の分岐
                if (color != "") {
                    mainHTML = "<div class=" + color + ">" + Ztable[Zk][Lv] + "</div>";
                } else {
                    mainHTML = Ztable[Zk][Lv];
                }

                if (A_SM != "none") {
                    Zcolumn.push(moneyHTML);//金額をcolumnにpush
                }

                Zcolumn.push(mainHTML);//メインをcolumnにpush
            }
        }

        // サブアイテム候補の出力
        for (var k = 0; k < 3; k++) {
            sub[k] = Stable.charAt(ran[j + k * 2 + 2] % 10);
        }//サブの候補 "PWT"
        var subCandidate = sub[0] + sub[1] + sub[2];
        //族を決める乱数の2,4,6個後の乱数を10で割った余りとサブテーブルで決める。
        Zcolumn.push(subCandidate);//サブ候補をcolumnにpush

        /*
          各スキルレベル毎のサブアイテムパターンの出力
        */
        //ここからスキルレベル毎のサブの個数パターンを出力します。現時点ではあやしいです。
        //for(sk=1;sk<6;sk++){//スキル１～５まで。０は意味無いので省略です。
        for (var s = 0; s < A_ES.length; s++) {
            var subItem = "";
            var sk = Number(A_ES[s]);

            function subPattern(P) {
                var deru = false;
                var pattern;
                if (ran[P] % 10 >= sk) {//サブ0個のパターンが存在
                    pattern = '+x';
                    deru = true;
                }
                if (ran[P - 1] % 10 < sk && ran[P] % 20 >= sk) {//サブ1個のパターンが存在
                    if (deru) {
                        pattern += ',+' + sub[0];//前に+xがあれば","を出力
                    } else {
                        pattern = '+' + sub[0];
                    }
                    deru = true;
                }
                if (ran[P - 2] % 10 < sk && ran[P - 1] % 20 < sk) {
                    if (ran[P] % 100 >= sk) {//サブ2個のパターンが存在
                        if (deru) {
                            pattern += ',+' + sub[0] + sub[1];//前に+xがあれば","を出力
                        } else {
                            pattern = '+' + sub[0] + sub[1];
                        }
                        deru = true;
                    } else {//サブ3個のパターンが存在
                        if (deru) {
                            pattern += ',+' + sub[0] + sub[1] + sub[2];//前に+xがあれば","を出力
                        } else {
                            pattern = '+' + sub[0] + sub[1] + sub[2];
                        }
                        deru = true;
                    }
                }
                if (!deru) {//サブ0個～3個どのパターンも存在しない。つまり取れない。
                    pattern = "---";
                }
                return pattern;
            }

            //北米版は金額に使われる乱数の個数が固定なので、サブアイテムが/左右に別れたりしない
            var subHTML = subPattern(j - 6)
            Zcolumn.push(subHTML); //サブアイテム出土候補をcolumnにpush
            //次のスキルレベルで繰り返し
        }//sのループここまで
        ZdataTable.push(Zcolumn);//これまでに作ったcolumnをZdataTableにpush
    } //iのループここまで

    self.postMessage(ZdataTable);
}, false);



