Title: Pythonのテストのパラメータ化にはparameterizedを使うと楽（unittestでもpytestでもnoseでも使えます）
Slug: parameterized
Date: 2017-8-16 0:48
Category: Python
Tags: Python, unittest

Pythonでテストをパラメータ化した時の書き方を [unittest](http://docs.python.jp/3/library/unittest.html) と [pytest](https://docs.pytest.org/en/latest/)
を使った場合で紹介し、最後にそれらで使えるparameterizedというライブラリを紹介します。


ちなみに私はpytestよりもunittest派です。

<!--more-->

## はじめに

テストを書いていると値が違うだけのケースを複数確認したくなる時があります。

例えば、1 + 1 = 2, 2 + 3 = 5, 32 + (-32) = 0, ...などのようなケースです。
これをすべて別のテストケースとして書き下すのは面倒ですしメンテも大変なことになるので、テストフレームワークは大抵こんなテストが簡単にできる仕組みを提供しています。

今回はPythonでよく使われているunittest（標準ライブラリ）とpytestでこれらのテストの書き方を紹介します。

なんでいまさら？と思われそうですが、pytestはともかくunittestでの書き方をあまり見かけなかったからです。

知ってる方は適当にparameterizedのところまで読み飛ばしてください。

## 今回書くテスト

2つの引数a, bを取って足し算して返す関数`add`の結果を確認するテストを考えます。

3通りのパラメータでテストします。
パラメータは入力をaとb, 期待される出力をansとして

- a=2, b=3, ans=4
- a=1, b=1, ans=3
- a=3, b=-1, ans=2

と残念な感じにします。
（テスト失敗時の出力を確認するためであって足し算できないとかではないです）

これをunittestで愚直に3通り書くと

```python
import unittest

def add(a, b):
    return a + b

class TestAdd(unittest.TestCase):
    def test_add_1(self):
        self.assertEqual(add(2, 3), 4)
    def test_add_2(self):
        self.assertEqual(add(1, 1), 3)
    def test_add_3(self):
        self.assertEqual(add(3, -1), 2)
```

明らかに面倒です。

少し凝った感じにすることもできますが、

```python
class TestAdd(unittest.TestCase):
    def test_add(self):
        for (a, b, ans) in ((2, 3, 4), (1, 1, 3), (3, -1, 2)):
            self.assertEqual(add(a, b), ans)
```

これは最初のケースで失敗して残りのテストが実行されません。


## テストのパラメータ化

### unittest の subTest

こんな時のためにunittestには[subTest](http://docs.python.jp/3/library/unittest.html#subtests)という機能があります。
（Python3.4で追加されました）

subTestを使って先ほどのテストを書き直します。

```python
class TestAdd(unittest.TestCase):
    def test_add(self) -> None:
        for a, b, ans in ((2, 3, 4), (1, 1, 3), (3, -1, 2)):
            with self.subTest(a=a, b=b, ans=ans):
                self.assertEqual(add(a, b), ans)
```

`with self.subTest(...)` がポイントです。

このテストを実行すると以下の出力が得られます。

[f:id:h-miyako:20170816162701p:plain]

途中で失敗してもテストが3通り実行され、きちんと失敗した2つのケースの詳細が表示されています。

とはいえ正直subTest書くの面倒なので今回紹介するparameterizedがなかったらpytest使ってたと思います。

### pytest の mark.parametrize

pytestでの同様のテストは次のようになります。

```python
import pytest

@pytest.mark.parametrize('a,b,ans', [
    (2, 3, 4),
    (1, 1, 3),
    (3, -1, 2),
])
def test_add(a, b, ans):
    assert add(a, b) == ans
```

pytestはテストケースが関数でかけるのですっきりしてますね。

テストケースの関数に`@pytest.mark.parametrize`デコレータをつけ、第一引数に引数の名前の文字列、第二引数にテストケースに与える値を列挙したリストを渡します。

実行結果は以下のとおりです。

[f:id:h-miyako:20170816162830p:plain]

### pytest の fixture

また、fixtureを使って間接的にパラメータを渡すこともできます。

```python
@pytest.fixture(params=[(2, 3, 4), (1, 1, 3), (3, -1, 2)])
def params(request):
    return request.param

def test_add(params):
    a, b, ans = params
    assert add(a, b) == ans
```

出力は次のようになります。

[f:id:h-miyako:20170816163114p:plain]

## parameterized を使った場合

正直、unittestのsubTestもpytestの方法も若干冗長で書くのが面倒な感じがしていました。

[parameterized](https://github.com/wolever/parameterized) というライブラリを使うと直感的にすっきりと書くことができます。

### インストール

`pip`でインストールします。

```
pip install parameterized
```

ちなみに **parameterized** とは別に **parametrized** というライブラリもPyPIに登録されているので注意してください（1敗）。
今回紹介する parameterized はバージョンが今日時点で0.6.1なのでインストール時にバージョン番号を確認すると確実だと思います。

### unittest + parametrized

次のように使います。

```python
from parameterized import parameterized

class TestAdd(unittest.TestCase):
    @parameterized.expand([
        (2, 3, 4),
        (1, 1, 3),
        (3, -1, 2)
    ])
    def test_add(self, a, b, ans) -> None:
        self.assertEqual(add(a, b), ans)
```

引数をタプルにしてリストで`@parameterized.expand`デコレータに渡すだけです。

出力は以下のようになります。

[f:id:h-miyako:20170816163406p:plain]

失敗した場合の値が表示されませんが、テストケースの名前の最後に0から順に連番がふられるので何番目のテストが失敗したのかはわかるようになっています。

### pytest + parametrized

pytestでは以下のようになります。

```python
from parameterized import parameterized

@parameterized([
    (2, 3, 4),
    (1, 1, 3),
    (3, -1, 2),
])
def test_add(a, b, ans):
    assert add(a, b) == ans
```

unittestの場合と違って `.expand` なしの `@parameterized` デコレータを使っていますがそれ以外は同じです。

出力は以下のようになります。

[f:id:h-miyako:20170816163430p:plain]

pytestでは初めて使いましたが出力にちゃんとパラメータが表示されてわかりやすいのいいですね……（unittest派）

### その他

parametrizedは他にもnose, nose2にも対応していてPythonの主要なテストフレームワークは網羅しています。
（元々はnose用のnose_parameterizedというライブラリでしたが、他のフレームワークにも対応して今の名前になりました。）

ここでは紹介しませんが、パラメータに名前付き引数を渡したり関数で渡すこともできたりけっこう高機能です。
それらの説明は[README](https://github.com/wolever/parameterized)にありますので気になった方はそちらをご確認ください。

## まとめ

unittestとpytestでテストをパラメータ化する方法とparameterizedを使った場合の書き方を紹介しました。

個人的な印象をざっくりまとめると

- unittest.subTest
    - めんどう
- pytest.mark.parametrize
    - subTestよりは楽だけど引数名書くの面倒
- parametrized
    - 楽

という感じでparameterizedおすすめです（特にunittestで書く時）。

次もunittestネタで何か書きます（予告）。
