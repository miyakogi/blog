Title: PythonでブラウザベースのGUIアプリを作るライブラリ、WDOMの紹介
Slug: wdom_intro
Date: 2016-4-6 20:00
Category: Python
Tags: python, wdom

WDOMというPythonでブラウザベースのGUIアプリを作るためのライブラリを作っています。
ちょっとしたGUIツールを作ろうと思った時に満足できるものがなかったので作りました。

[miyakogi/wdom: DOM manipulation library for python](https://github.com/miyakogi/wdom)

WDOMのターゲットは、あくまでブラウザベースのデスクトップGUIアプリです。
ローカルにWebサーバを立ち上げてブラウザ上に表示しますが、Webフレームワークではありません。
ちなみに、拙作[LiveMark.vim](https://github.com/miyakogi/livemark.vim)もこれを使っています。

まだ開発中なので細かいバグはあると思いますし、後方互換性を崩すような変更が入る可能性もありますが、そろそろ試してもらえるくらいにはなってきたので使い方を中心に紹介します。

もしバグを発見したら[GitHubのIssue](https://github.com/miyakogi/wdom/issues)に報告していただけると助かります。

- 関連記事
    - [WDOMのテーマ機能と起動オプションの紹介 - Blank File](http://h-miyako.hatenablog.com/entry/2016/05/02/180543)

<!--more-->

- 2016/05/01:追記
    - 要素の属性アクセスについて記述を追加
    - `style`属性について記述を追加
    - JavaScriptを実行する方法を追加

- 2017/08/11:編集
    - 最近のアップデートを反映

## 動機

PythonのGUIライブラリだと標準ライブラリのTkInterやPyQt、wxPythonなどが有名で、私はPyQtを結構使っていましたが、以下の不満もありました。

- 見た目が残念（他よりマシですが、今となっては・・・）
    - スタイルの変更は一応可能ですが面倒です
    - いい感じのCSSを読み込んでクラス指定くらいで済ませたいです
- インストールが大変
    - `pip install PyQt`では今の所インストールできません
        - [2016/04/28 追記] [できるようになった](https://www.riverbankcomputing.com/pipermail/pyqt/2016-April/037388.html)ようです
    - anacondaなどで楽できるらしいですが好きじゃないです
- 配布可能なバイナリパッケージにするのもそれなりに面倒
    - だいぶ記憶が薄れてしまいましたが、いくつかはまった記憶があります
        - 特にWindows・・・
- 情報が少ない
    - 結局qtのリファレンスを読みながら使っていました
- テストしにくい
    - UIが絡むテストも[できるらしい](http://johnnado.com/pyqt-qtest-example/)ですが
- ライセンスがGPL
    - 自分が使う分には問題ありませんが、やっぱりもっとゆるいライセンスが気持ち的に安心です

## 特徴

ということで、WDOMは上記の不満をそれなりに解消するために作りました。

ブラウザ上に表示するので各種CSSライブラリなどはそのまま使えますし、メソッド名などもDOMと同じなので学習コスト低め（調べたことが無駄になりにくい）です。
基本的には、PyQtでよく使う機能はDOMで実現できるでしょたぶん、という方針です。

- ブラウザ上に表示するので、巷に溢れるCSSフレームワークが利用可能
    - Bootstrap万歳
- 必須ライブラリはtornadoだけ、かつpure python実装なのでインストールはpipでOK
- 配布可能なバイナリにするのも通常のpythonで書かれたパッケージと（だいたい）同じ方法でOK
- インターフェイスはDOM仕様に基づいているので、メソッド名や引数のとり方などは[MDN](https://developer.mozilla.org/ja/docs/Web/API)などで確認可能
    - `Element.appendChild(追加したい要素)` で追加とかする感じです
        - イベントの処理は`Element.addEventListener('click', 関数)`です
        - 実装済みの機能は[こちら](https://github.com/miyakogi/wdom/wiki/Features)をご参照ください
    - JavaScriptでDOMを触ったことがあればなんとなくわかると思います
    - JavaScriptを触ったことがなくても、今後触る機会があるかもしれないので、覚えたことは無駄になりにくいです
    - まだブラウザに実装されていない最新のDOM仕様も一部実装しています
        - [ChildNode](https://developer.mozilla.org/ja/docs/Web/API/ChildNode)のbefore/afterや[ParentNode](https://developer.mozilla.org/ja/docs/Web/API/ParentNode)のappend/prependなど
        - Custom Elementsも一応実装しています
- [Selenium](http://selenium-python.readthedocs.org/)でUIのテストが可能
    - Seleniumもブラウザ上でテストを実行する汎用的なライブラリなので、覚えたことは無駄になりにくいです
    - HTMLを出力して確認することもできます
- ライセンスはMITです

類似のプロジェクトでは[flexx](https://github.com/zoofIO/flexx)や[Reahl](http://www.reahl.org/)などがありましたが、これらはそれなりに学習コストが高そう＆Webフレームワークっぽかったので見送りました。

## 必要環境

Python 3.5.2以上の対応です。
おそらく大丈夫だとは思いますが、Windows環境ではテストしていません。

ブラウザ上に表示するのでブラウザが必要です。
逆に言えば、Pythonが動作してブラウザがある環境であれば動作します。
当然ですがIEはサポート対象外です。
とはいえ、ほとんどの機能は動作すると思います。
ブラウザはElectronやPyQtのブラウザなどでも大丈夫です（たぶん）。

## インストール

普通にpipでインストールできます。

```
pip install wdom
```

最新版はgithubから

```
pip install git+http://github.com/miyakogi/wdom
```

Webフレームワークの[tornado](http://www.tornadoweb.org/en/stable/)に依存しているので一緒にインストールされます。
オプションで[aiohttp](http://aiohttp.readthedocs.org/en/stable/)を使うこともできます。
こちらはネイティブでasyncioに対応していますし、C拡張で書かれているので（たぶん）パフォーマンス的にも優位だと思います。

```
pip install aiohttp
```

aiohttpがインストールされていれば勝手にそっちを使うので、特別な設定は必要ありません。

2017/08/11: aiohttpのサポートは取りやめました。

## 基本的な使い方

とりあえず "Hello, WDOM" と表示するだけのプログラムは以下のようになります。

```python
from wdom import server
from wdom.document import get_document
from wdom.tag import H1

if __name__ == '__main__':
    document = get_document()  # documentオブジェクトを取得
    h1 = document.createElement('h1')  # 'h1' タグを作る
    h1.textContent = 'Hello, WDOM'  # 'h1' タグの文字列を指定
    document.body.appendChild(h1)  # 'body' タグに 'h1' タグを挿入
    setver.start()  # webサーバ立ち上げ
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut1.py)

このプログラムを実行して、ブラウザで`http://localhost:8888`にアクセスすると "Hello, WDOM" と表示されるはずです。

重要な部分は `document = get_document()` 以下の4行です。
ほぼJavaScriptでDOMを操作する時と同じになっています。
要素の追加は[appendChild](https://developer.mozilla.org/ja/docs/Web/API/Node/appendChild)や[insertBefore](https://developer.mozilla.org/ja/docs/Web/API/Node/insertBefore)、[replaceChild](https://developer.mozilla.org/ja/docs/Web/API/Node/replaceChild)などで行えます。
[removeChild](https://developer.mozilla.org/ja/docs/Web/API/Node/removeChild)で削除することも可能です。

「`document.createElement` とか面倒」と感じると思いますが、ショートカットは用意してあるのでご安心下さい（後述します）。
また、ここでは`appendChild`で要素を追加していますが、[最新の仕様](https://dom.spec.whatwg.org/)に含まれている`append`や`after`、`remove`なども実装してあります。

## DOMについて

WDOMで扱うUI部品はすべてブラウザ上のタグ（要素）に相当します。
WDOMの各要素はブラウザ上のタグと一対一の関係を持っています。

例えば、上の例で作った`h1`要素（`docuemnt.createElement('h1')`で作られたインスタンス）はブラウザ上のh1タグ、すなわち`<h1></h1>`というHTMLの要素になります。
WDOMのUI部品はHTMLで表現することができ、実際にブラウザ上で表示されるHTMLは`html`属性で取得することができます。
先ほどの`h1`要素であれば`print(h1.html)`とすることで実際のHTMLを確認できます。

これらの要素はDOMで規定されている各種メソッドも備えているので、JavaScriptでDOMを扱う時と同じように要素の追加・削除などを行うことができます。

この節では基本的なDOM操作について説明します。
ブラウザ上のJavaScriptとほとんど同じなので、そちらをご存じの方は読み飛ばしてください。
WDOMに実装済みの機能は[機能の一覧](https://github.com/miyakogi/wdom/wiki/Features)または後述する`Tag`クラスの[APIドキュメント](https://miyakogi.github.io/wdom/tag.html)に一覧があります。

### 要素の作成

WDOMで要素を新規に作成する方法は、大別して以下の三種類の方法があります。

- `docuemnt.createElement` メソッドでタグ名を指定して作成
- 各要素の`innerHTML`や`insertAdjacentHTML`でHTMLから作成
- `wdom.tag`モジュールで定義されている各クラスから作成

作成された要素は、`document`をルートとするDOMツリーに追加されるまでは表示されません。
ただし、`innerHTML`や`insertAdjacentHTML`では作成と同時にその要素の子要素として追加されます。

- 参考
    - [document.createElement  MDN](https://developer.mozilla.org/ja/docs/Web/API/Document/createElement)
    - [element.innerHTML MDN](https://developer.mozilla.org/ja/docs/Web/API/Element/innerHTML)
    - [element.insertAdjacentHTML MDN](https://developer.mozilla.org/ja/docs/Web/API/Element/insertAdjacentHTML)

### 要素の追加

`appendChild`や`insertBefore`メソッドで要素をDOMツリーに追加することができます。

`親要素.appendChild(追加する要素)`では、親要素の最後の子要素として`追加する要素`が追加されます。

`親要素.insertBefore(追加する要素, 追加したい位置の要素)`では、`追加したい位置の要素`の直前に`追加する要素`が挿入されます。
`追加したい位置の要素`は親要素の直接の子要素でなくてはなりません。

追加された要素がすでに別の親要素を持っていた場合、その親要素からは自動的に取り除かれます。

- 参考
    - [Node.appendChild MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/appendChild)
    - [Node.insertBefore MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/insertBefore)

### 要素の削除

`removeChild`メソッドで特定の子要素を削除することができます。

`親要素.removeChild(子要素)`とすることで、子要素は親要素から取り除かれます。
この時、取り除かれる子要素は親要素の直接の子要素でなくてはなりません。

- 参考
    - [Node.removeChild MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/removeChild)

### 要素の入れ替え

`replaceChild`メソッドで要素子要素を入れ替えることができます。

`親要素.replaceChild(挿入する要素, 取り除く要素)`とすることで、`取り除く要素`が`挿入する要素`と置き換えられます。
この時、`取り除く要素`は親要素の直接の子要素でなくてはなりません。

- 参考
    - [Node.replaceChild MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/replaceChild)

### 親要素へのアクセス

ある要素の親要素には`要素.parentNode`属性でアクセスできます。
要素がまだDOMツリーに追加されておらず、親要素が存在しない場合は`None`を返します。

- 参考
    - [Node.parentNode MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/parentNode)

### 子要素へのアクセス

ある要素の子要素には`要素.childNodes`属性でアクセスできます。

`childNodes`属性で返されるオブジェクトはリスト風の**Live Object**です。
Pythonのリスト同様、`for child in 要素.childNodes:`という形でループを介してアクセスしたり、`childNodes[i]`という形でインデックスアクセスしたり、`if child in parent.childNodes:`などの形で特定の要素が含まれているか確認することができます。

ただし、通常のリストとは異なり、直接要素を追加したり削除したりすることはできません。
また、**Live Object**なので、親要素の変更が常時反映されます。
そのため、以下のようなコードは無限ループになってしまいます。

```python
p = docuemnt.createElement('div')
p.appendChild(docuemnt.createElement('p'))
child_nodes = p.childNodes
for n in child_nodes:
    p.appendChild('p')
```

先頭の子要素、あるいは末尾の子要素には`要素.firstChild`や`要素.lastChild`でアクセスすることもできます。
子要素が存在しない場合、これらは`None`を返します。

- 参考
    - [Node.childNodes MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/childNodes)
    - [Node.firstChild MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/firstChild)
    - [Node.lastChild MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/lastChild)

### 隣接ノードへのアクセス

隣接するノードには`nextSibling`や`previousSibling`でアクセスできます。
親要素を持たない場合、または要素が先頭・末尾にあって該当する要素が存在しない場合は`None`を返します。

- 参考
    - [Node.nextSibling MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/nextSibling)
    - [Node.previousSibling MDN](https://developer.mozilla.org/ja/docs/Web/API/Node/previousSibling)

### 属性値へのアクセス

各要素にはHTML同様に属性値を設定することができます。
HTMLの`<a href="http://......./">リンク</a>`における`href=""`に相当する部分です。

`getAttribute('属性名')`で取得、`setAttribute('属性名', '値')`で設定、`removeAttribute('属性名')`で削除できます。
存在しない属性に対して`getAttribute`を行うと`None`または空文字列(`''`)、`False`など属性毎の規定に従った値が返されます。

- 参考
    - [Attr MDN](https://developer.mozilla.org/en-US/docs/Web/API/Attr)
    - [element.getAttribute MDN](https://developer.mozilla.org/ja/docs/Web/API/Element/getAttribute)
    - [element.setAttribute MDN](https://developer.mozilla.org/ja/docs/Web/API/Element/setAttribute)
    - [Element.removeAttribute() MDN](https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttribute)
    - [NamedNodeMap MDN](https://developer.mozilla.org/ja/docs/Web/API/NamedNodeMap)

#### 使用例

```python
a = docuemnt.createElement('a')
a.textContent = 'リンク'
a.setAttribute('href', '/')
print(a.html) # <a href="/">リンク</a>`
print(a.getAttribute('href')) # '/'
a.removeAttribute('href')
print(a.getAttribute('href')) # None
```

各要素に設定されている属性の一覧は`要素.attributes`で取得することができます。
この時返されるオブジェクトは`{'属性名': Attrノード, ...}`の辞書風オブジェクト（NamedNodeMap）です。

### 特殊な属性値

一部の属性値は、要素の属性（プロパティ）として直接アクセスすることができます。

例えば`id`属性は`要素.id`で取得したり`要素.id = 'some_id'`で設定することができます。
`getAttribute`メソッドで属性値を取得した場合、属性が存在する場合の返り値は文字列型で属性が存在しない場合は`None`が返されますが、プロパティから取得した場合の型は属性によって異なります。
`id`属性の場合、設定されていない状態では`要素.id`を取得すると（`None`ではなく）空文字列が返ります。

その他、例えば`hidden`属性は`True`または`False`の真偽値を返しますし、`style`属性は`CSSStyleDeclaration`のインスタンスを返します。

`hidden`属性の様に真偽値を返すプロパティは、プロパティから値を設定した場合と`setAttribute`メソッドで値を指定した場合の振る舞いが直感とは異なるので注意が必要です。
`a=document.createElement('a'); a.hidden = True; a.html == '<a hidden></a>'`という要素を例に挙げると、`a.hidden = False`と設定すると`a.html == '<a></a>'`と`hidden`属性は削除されますが、`a.setAttribute('hidden', False)`では`hidden`属性は削除さず、`a.html == '<a hidden></a>'`のままです。
`a.hidden = False`と同じように属性値を削除するためには、`a.removeAttribute('hidden')`として属性値を削除する必要があります。
（正直微妙な気はしますが）これはブラウザJSの挙動と（ほぼ）同じです。

また、`style`属性は`CSSStyleDeclaration`を返しますが、属性値の設定は文字列で行うことができます。
つまり`a.style = 'color: red;'`という様にスタイルを指定することができます。
ただし上記の方法だとすでに`style`属性が設定されていた場合に既存のスタイルを削除してしまいます。
スタイルに修正を加える場合は、`a.style.color = 'red'`などのように`style`属性が返す`CSSStyleDeclaration`に対して行う方が安全でしょう。

`CSSStyleDeclaration`は各CSSプロパティ（`color`や`background`など）にプロパティアクセスできます。
`-`を含むプロパティ（`background-color`や`margin-bottom`）などは`-`直後の文字を大文字にして`-`を取り除く（`a.style.backgroundColor`や`a.style.marginBottom`など）ことでアクセスできます。
ほとんどのCSSプロパティはこのルールが適用されますが、`float`の様に一部異なるものも存在します。
とはいっても、現時点でWDOMで実装されているのは`float`属性だけです。他にもありましたらご指摘下さい。
詳細は[CSS Properties Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Properties_Reference)を参照して下さい。

- 参考
    - [HTMLElement](https://developer.mozilla.org/ja/docs/Web/API/HTMLElement)
    - [element.id](https://developer.mozilla.org/ja/docs/Web/API/Element/id)
    - [element.style](https://developer.mozilla.org/ja/docs/Web/API/HTMLElement/style)
    - [CSS Properties Reference](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Properties_Reference)

### イベント

イベント処理の追加には`addEventListener`メソッドを使用します。
実際に動かしたほうがわかりやすいと思うので、最初のサンプルコードをベースに説明します。

#### クリック時に文字列反転

上記のサンプルコードで、`h1.textContent = ...` の次の行に以下のコードを追加してみてください。

```python
    def rev_text(event):
        # h1の中身の文字列を反転
        h1.textContent = h1.textContent[::-1]
    h1.addEventListener('click', rev_text)  # rev_textには括弧なしです！
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut2.py)

`h1`要素がクリックされた時に文字列が反転するはずです。

`addEventListener`の第一引数が反応するイベントの種類（文字列）、第二引数がそのイベントが発火した時に実行される処理（関数、イベントリスナー）になります。
[JavaScriptの場合と同じ](https://developer.mozilla.org/ja/docs/Web/API/EventTarget/addEventListener)です。
今回はクリックされた時に`rev_text`関数を実行し、h1要素の中身の文字列を反転させています。
`rev_text`関数には`Event`オブジェクトが渡されますが、今回は使っていません。

- 参考
    - [EventTarget.addEventListener MDN](https://developer.mozilla.org/ja/docs/Web/API/EventTarget/addEventListener)

#### ユーザー入力の取得

ユーザーからの入力を取得したい場合は、`input`要素または`textarea`要素を使います。
input要素に入力された文字列を、先ほどのh1要素に表示してみます。

以下のように変更してください。

```python
    document = get_document()
    h1 = document.createElement('h1')
    h1.textContent = 'Hello, WDOM'
    input = document.createElement('input')
    def update(event):
        h1.textContent = event.currentTarget.value
    input.addEventListener('input', update)
    document.body.appendChild(input)
    document.body.appendChild(h1)
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut3.py)

文字列を入力すると "Hello, WDOM" と表示されていた部分が置き換えられるはずです。

`update`関数内でアクセスしている`event.currentTarget`は、イベントの対象となっているオブジェクトへの参照（この場合はinput要素）です。
[input要素](https://developer.mozilla.org/ja/docs/Web/API/HTMLInputElement)は現在の入力値を`value`属性に保持しているので、それをh1要素の`textContent`に設定しています。

`event`オブジェクトもDOMの[Event](https://developer.mozilla.org/ja/docs/Web/API/Event)オブジェクトと同じ構造をしているので、詳細は仕様を確認してください。
現在、`Event`、`MouseEvent`、`KeyboardEvent`、`DragEvent`が実装済みです。

- 参考
    - [Event MDN](https://developer.mozilla.org/ja/docs/Web/API/Event)
    - [Event reference MDN](https://developer.mozilla.org/en-US/docs/Web/Events)

#### イベントリスナーの削除

登録したイベントリスナーを削除する場合は`removeEventListener`を使います。

`addEventListener`同様、`removeEventListener(イベントの種類, イベントリスナー)`の形で呼び出し、イベントの種類とイベントリスナーの両方が一致した時にそのイベントリスナーが取り除かれます。

- 参考
    - [EventTarget.removeEventListener MDN](https://developer.mozilla.org/ja/docs/Web/API/EventTarget/removeEventListener)

## Pythonのクラスの利用

毎回`createElement`をするのはとてつもなく面倒ですし、documentへの参照が必要で不便極まりないので、クラスから直接要素を作れるようにしてあります。
以下の機能は[BeautifulSoup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)を参考にしました。

例えば、先ほどのh1要素とinput要素を子要素に持つdiv要素を作る場合は以下のようにできます。

```python
from wdom.tag import Div, H1, Input

class MyElement(Div):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h1 = H1()  # h1要素を新しく作成
        self.h1.textContent = 'Hello, WDOM'
        self.input = Input()  # input要素を新しく作成
        self.input.addEventListener('input', self.update)
        self.appendChild(self.input)
        self.appendChild(self.h1)

    def update(self, event):
        self.h1.textContent = event.currentTarge.value

if __name__ == '__main__':
    ... # 省略

    document = get_document()
    document.body.appendChild(MyElement())
    ... # 以下同じ
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut4.py)

[wdom.tagモジュール](https://github.com/miyakogi/wdom/blob/dev/wdom/tag.py)には一般的なタグを表すクラスが一通り定義してあります。
全てタグ名の一文字目が大文字で他は小文字というクラス名です。

例えば`<button>`タグは`wdom.tag.Button`で`<br>`タグは`wdom.tag.Br`です。
例外はありません。
`textarea`も`wdom.tag.Textarea`です。

上記の`MyElement`クラスのように、既存のクラスを継承して独自のクラスを作ることもできます。
`MyElement`クラスは`Div`クラスを継承しているので、そのインスタンスはブラウザ上では`<div>`要素として表示されます。

`print(MyElement().html)`とすると実際のhtmlが取得できます。
この場合、以下のようになっているはずです。

```html
<div wdom_id="数値〜"><input wdom_id="数値〜"><h1 wdom_id="数値〜">Hello, WDOM</h1></div>
```

`wdom_id`は内部で使っている属性です。
無視して下さい。
テストなどで邪魔な場合は、`html_noid`を使うと`wdom_id`を除いたhtmlが取得できます。

```python
print(MyElement().html_noid)
# -> <div><input><h1>Hello, WDOM</h1></div>
```

### 親要素に自動的に追加

毎回appendChildを呼び出すのも面倒なので、インスタンス生成時に`parent`引数で親要素を指定できるようにしてあります。

先ほどの例は以下のように書き換えることができます。
（要素の追加される順番が先ほどと違ってしまいますが）

```python
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h1 = H1(parent=self)  # h1要素を新しく作成して自分の子要素にする
        self.h1.textContent = 'Hello, WDOM'
        self.input = Input(parent=self)  # input要素を新しく作成して自分の子要素にする
        self.input.addEventListener('input', self.update)
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut5.py)

### 子要素を自動的に追加

逆に、子要素をインスタンス作成時に追加することもできます。

```python
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 子要素として'Hello, WDOM'を持つh1要素を新しく作成し、子要素に追加
        self.h1 = H1('Hello, WDOM', parent=self)
        self.input = Input(parent=self)  # input要素を新しく作成して自分の子要素にする
        self.input.addEventListener('input', self.update)
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut6.py)

`H1('Hello, WDOM', parent=self)`としている部分では、第一引数が新しく作られる要素の子要素に追加されます。
文字列は自動的に[Textノード](https://developer.mozilla.org/ja/docs/Web/API/Text)（`wdom.node.Text`）に変換されます。
`Div(H2(), P(), ...)`として複数の要素を追加することも可能です。

### 属性値を設定

インスタンス化する時に属性値を設定することもできます。

```python
input = Input(type='checkbox')
print(input.html_noid)  # <input type="checkbox">

# JavaScript同様、以下のようにして設定することも可能です
input = Input()
input.setAttribute('type', 'checkbox')
# または input.type = 'checkbox'
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut7.py)

`class`属性はpythonの予約語とかぶっているので、`class_`と末尾にアンダースコアをつけてください。

```python
h1 = H1(class_='title')
print(h1.html_noid)  # <h1 class="title"></h1>

# 以下と同じです
h1 = H1()
h1.setAttribute('class', 'title')
# または h1.classList.add('title')
# classList は複数追加可能です
# h1.classList.add('title', 'heading', ...)
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut8.py)

### デフォルトのクラス属性を設定

よく使うタグとクラス属性の値をまとめて定義しておくことも可能です。

例えばbootstrapのボタンはクラスに`class="btn"`と指定する必要がありますが、これをデフォルトで定義されている(pythonの)クラスを作ることができます。

```python
from wdom.tag import Button

class MyButton(Button):
    class_ = 'btn'
    ... # 省略

print(MyButton().html_noid)
# <button class="btn"></button>
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut9.py)

クラス変数の`class_`に指定したクラス属性が自動的に設定されます。
これは以下のように定義した場合とほぼ同じです。

```python
class MyButton(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setAttribute('class', 'btn')
        ...
```

違いは、インスタンスから削除できないという点と、クラス変数として定義したクラス属性はサブクラスに継承されるという点です。

前者は以下のような操作ができないことを意味します。

```python
btn = MyButton()
btn.classList.remove('btn')  # classListから'btn'クラスを削除しようとしても
print(btn.html_noid)  # <button class="btn"></button>  # 削除されない
```

後者の継承されるという点は文字通りですが、継承されたクラスで`class_`と指定しても置き換えられず、追加されます。
例えば`DefaultButton`というクラスを作り、`class="btn btn-default"`というクラス属性を持たせたい場合は、

```
class DefaultButton(MyButton):
    class_ = 'btn-default'
```

とするだけでクラス属性を追加することができます。

```python
db = DefaultButton()
print(db.html_noid)  # <button class="btn btn-default"></button>
```

### class定義のショートカット

クラス属性が違うだけの(Pythonの)クラスを`class`文でいくつも定義するのは面倒なので、簡単に定義するための`wdom.tag.NewTagClass`という関数を用意しました。

この関数を使うことで、先ほどの`MyButton`や`DefaultButton`は次のように定義することができます。

```python
from wdom.tag import Button, NewTagClass

MyButton = NewTagClass('MyButton', 'button', Button, class_='btn')
DefaultButton = NewTagClass('DefaultButton', 'button', MyButton, class_='btn-default')
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut10.py)

`NewTagClass`の第一引数は新しく作るクラスの名前、第二引数はタグ、第三引数は継承するクラス、第四引数以降の名前付き引数はクラス変数になります。
第三引数はタプルで複数のクラスを指定することも可能です。

これらの機能はDOM仕様ではなく独自仕様ですが、JavaScriptとPythonの違い、利便性等を考慮して実装しました。
独自仕様なので今後変更される可能性もあります。
ご注意ください。
（クラス変数の`class_`は`classes`にしてリストでクラスを指定する形にしたい気持ちもあります）

### 任意のJavaScriptコードの実行

JavaScriptライブラリを併用してJavaScriptの実行が必要になる場合もあると思いますが、（現時点では）動的に`script`要素を追加してもブラウザによっては実行されません。
これはブラウザの仕様にも依存しているのですが、最近のブラウザは`script`要素を`innerHTML`など書き換えても実行されないものもあるためです。
（WDOMでは要素の追加時にブラウザ上で`insertAdjacentHTML`を使っているのが原因なので、今後各ブラウザの実装状況を鑑みながら修正したいとは考えています。）

そこで、WDOMではブラウザ上でJavaScriptを実行するため、各要素（Element）に`exec`というメソッドを用意しています。
（メソッド名は今後変更される可能性があります。）

`exec`メソッドは文字列を引数としてとり、与えられた文字列をJavaScriptとしてブラウザ上で実行します。
例えば、以下のコードでは`button`要素がクリックされた時にアラートが表示されます。

```python
from wdom.tag import Button
button = Button('click')
def clicked(e):
    button.exec('alert("clicked!");')
button.addEventListener('click', clicked)
```

この例では一行の処理ですが、複数行でも実行可能です。

`exec`で実行されるスクリプト内では`this`（または`node`という変数）で自身（ブラウザ上の対応するDOM）にアクセスすることができます。
これは以下のJavaScriptをブラウザ上で実行しているのと等価です。

```javacript
var node = (execを呼び出した要素)
function() {
    eval(execに与えられた文字列)
}.bind(node)()
```

`window`や`document`などのブラウザ上のオブジェクトにアクセスすることや、事前に読み込ませたJavaScriptで定義された関数を実行することも可能です。

## HTMLでの記述

構造を上記のような`appendChild`などだけで作っていくのは大変なので、HTMLで記述してパースできるようにしてあります。
JavaScriptと同様、`innerHTML`でHTML文字列を設定するだけです。

例えば大きなリストを作る時は以下のようにすることができます。

```python
from wdom.tag import Ul
ul = Ul()
ul.innerHTML = '''
<li>...</li>
<li>...</li>
<li>...</li>
<li>...</li>
'''
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut11.py)

`innerHTML`は既存の子要素を全て削除して置き換えます。

各子要素にはリスト風オブジェクトの`ul.childNodes`経由でアクセス可能です。
`ul.firstChild`や`ul.lastChild`などで最初・最後の子要素にもアクセスできます。
これもJavaScript（というかDOMの仕様）と同じです。
（上の例だと改行だけのTextノードも作られてしまうのですが、一応Chromeでの動作と同じです。）

また、`insertAdjacentHTML(position, html)`メソッドでもHTMLをパースできます。
このメソッドは既存の子要素は削除せず、`position`で指定した位置に要素を挿入します。
詳細は[element.insertAdjacentHTML MDN](https://developer.mozilla.org/ja/docs/Web/API/Element/insertAdjacentHTML)などをご参照ください。

なお`outerHTML`は未実装です。

## スタイルシートの適用

デフォルトの表示は寂しいので、スタイルシートを適用しましょう。
見栄えは重要です。

### Web上のリソース読み込み

例としてBootstrapを使ってみます。

Bootstrapの場合はcssとjavascript二つ（bootstrapとjquery）が必要なので、それぞれ`<head>`要素と`<body>`要素に追加します。

```python
from wdom.tag import Link, Script, Button

document = get_document()
# <head>内にbootstrap.min.cssを読み込むlinkタグを追加
document.head.appendChild(Link(rel='stylesheet', href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css'))

# <body>にjqueryとbootstrap.min.js追加
document.body.appendChild(Script(src='https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js'))
document.body.appendChild(Script(src='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js'))

# ボタン追加
document.body.appendChild(Button(class_='btn'))
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut12.py)

CSSとJSは頻繁に使われると思うので、以下のショートカットも用意してあります。

```python
document.add_cssfile('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css')
document.add_jsfile('https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js')
document.add_jsfile('https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js')
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut13.py)

### ローカルのファイル読み込み

独自に作ったcssファイルなどを読み込むことも可能です。

例えば以下のようなディレクトリ構成で、`app.py`から`static/css/app.css`を読み込む場合を考えます。

```
.
├── static
│   └── css
│       └── app.css
├── app.py
├── module1.py
├── ...
...
```

`app.py`で次のように指定します。

```python
from os import path

static_dir = path.join(path.dirname(path.abspath(__file__)), 'static')
document = get_document()
document.add_cssfile('/static/css/app.css')
app = get_app(document)
app.add_static_path('static', static_dir)
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut14.py)

`app.add_static_path()`の第一引数は、静的ファイルへアクセスする時のprefixになります。
指定したディレクトリ以下のファイルに`http://localhost:8888/{prefix}/{ファイル名}`でアクセスできるようになります。
上記の例では`http://localhost:8888/static/css/app.css`とアクセスするとapp.cssが表示されるはずです。

prefixとディレクトリ名は異なっていても大丈夫です。
例えば`add_static_path('my_static', static_dir)`とすることもでき、この場合は`document.add_cssfile('/my_static/css/app.css')`とすることで`app.css`を読み込むことができます。
ブラウザで`http://localhost:8888/my_static/css/app.css`にアクセスすると、実際のcssファイルが表示されることが確認できるはずです。

cssやjsファイルに限らず、画像やhtmlなどの静的ファイルでも何でも利用可能です。

なお、prefixはurlに使える値なら何でも構いませんが、`_static`というprefixだけはライブラリ側で使っているので他の名前を使ってください。

## DOMの便利な新機能

まだブラウザに実装されていない機能もいくつか実装しているので紹介します。

### ParentNode/ChildNode インターフェイスの各メソッド

`appendChild`は単一の要素しか追加できませんが、`append`というメソッドでは複数の要素をまとめて追加できます。
さらに、文字列も自動的にTextノードに変換されます。

```python
from wdom.tag import Ul, Li
ul = Ul()
li1 = Li()
li2 = Li()
...
ul.appendChild(li1)
ul.appendChild(li2)
...

# appendを使うと
ul.append(li1, li2, ...)
# と一度で終わる
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut15.py)

同様に、先頭にまとめて追加する`prepend`や、前後に追加する`after`や`before`も利用可能です。

内部的には、`appendChild`などは毎回通信を行ってブラウザ上の表示を更新しているのに対し、`append`などでは一度に表示を更新しているので、パフォーマンス的にも有利です。

- 参考
    - [ParentNode MDN](https://developer.mozilla.org/ja/docs/Web/API/ParentNode)
    - [NonDocumentTypeChildNode MDN](https://developer.mozilla.org/ja/docs/Web/API/NonDocumentTypeChildNode)
    - [ChildNode MDN](https://developer.mozilla.org/ja/docs/Web/API/ChildNode)
    - [ParentNode DOM Standard](https://dom.spec.whatwg.org/#interface-parentnode)
    - [NonDocumentTypeChildNode DOM Standard](https://dom.spec.whatwg.org/#nondocumenttypechildnode)
    - [ChildNode DOM Standard](https://dom.spec.whatwg.org/#interface-childnode)

### Custom Element

独自タグも限定的・実験的ですがサポートしています。
ブラウザ上では特に何もせず、`innerHTML`などでhtmlをパースした時に作られるPythonのクラスを指定できるだけですが。。。

WebComponentsの仕様自体が流動的なので、今後変更される可能性はあります。

#### 独自タグの定義

先ほど作った`MyElement`クラスは`div`タグとして表示されていましたが、独自の`<my-element>`タグとして定義してみます。

```python
from wdom.tag import Div

class MyElement(Div):
    # 独自タグを'my-element'と指定
    tag = 'my-element'
    def __init__(self, *args, **kwargs):
        ... # 省略
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut16.py)

違いはクラス変数として`tag = 'my-element'`と設定していることだけです。
先ほどと同様に`Div`クラスを継承していますが、特に意味はありません。
`Span`などでも大丈夫です。

これをCustom Tagとして登録します。

```python
document.defaultView.customElements.define('my-element', MyElement)
```

以前のCustom Elementの仕様では`docuemnt.registerElement`というメソッドが使われていましたが、[最新の仕様](http://w3c.github.io/webcomponents/spec/custom/)では`window.customElements.define`というメソッドを使うようになっていたので、wdomもそちらに合わせました。
`document.defaultView`はブラウザ上での`window`オブジェクトに相当します。
（現状のWDOMではほとんど空のオブジェクトになっていますが・・・）

これで`my-element`という独自タグが登録できたので、以下のように使うことができます。

```python
# body要素の末尾に <my-element></my-element> を挿入
document.body.insertAdjacentHTML('beforeend', '<my-element></my-element>')
# または、createElementで新規作成
my_element = document.createElement('my-element')
```

#### 既存タグの拡張

`is`属性を使った既存タグの拡張にも対応しています。
前述したbootstrapのbutton要素の`MyButton`や`DefaultButton`を定義してみます。

```python
from wdom.tag import Button, Div

class MyButton(Button):
    # tag = 'button'
    class_ = 'btn'
    is_ = 'my-button'  # tag ではなく is_ に名前を指定

class DefaultButton(MyButton):
    class_ = 'btn-default'
    is_ = 'default-button'

document.defaultView.customElements.define('my-button', MyButton, {'extends': 'button'})
document.defaultView.customElements.define('default-button', DefaultButton, {'extends': 'button'})

div = Div(parent=document.body)
div.innerHTML = '<button is="my-button"></button><button is="default-button"></button>'
print(isinstance(div.firstChild, MyButton))  # True
print(isinstance(div.lastChild, DefaultButton))  # True
```

[サンプルコード](https://github.com/miyakogi/wdom_tutorial_ja/blob/master/tut17.py)

(Pythonの)クラス定義時にクラス変数の`is_`（最後にアンダースコア）で名前を指定します。
tagは拡張したいタグ（今回は継承元の`Button`クラスで定義されているので指定不要）です。

定義したクラスを登録する時に、`define`の第一引数に名前（`is_`の値）を指定し、第三引数に辞書で`{'extends': 'button'}`と拡張したい元のタグ名を指定します。

このように登録することで、`<button is="my-button">`などのhtmlから`MyButton`クラスのインスタンスが作られるようになります。

（タグとisの指定がわかりにくく、いかにも混乱しそうですが、今の所こういう仕様なのでそれに合わせています）

#### Custom Elementを使う上での注意

できるだけ早い段階で独自タグを定義するようにしてください。
定義前にインスタンスを作ってしまうと、異なるクラスのインスタンスが作られてしまいます。
一応`customElements.define`で登録された時に無理やりクラスは置き換えていますが、`__init__`は呼ばれません。
特に、`is`を使った既存タグの拡張は、インスタンスを作った後に`setAttribute('is', '...')`などとしても（現時点では）クラスは変更されないので注意してください。

今後[ライフサイクルコールバックメソッド](http://www.html5rocks.com/ja/tutorials/webcomponents/customelements/#lifecycle)に相当する機能は作りたいと考えていますが、事前に登録を済ませておいたほうが安全なのは変わらないと思います。


## おわりに

長くなってしまいましたが、お読みいただきありがとうございました。

説明が必要な独自機能を中心に書いたので、あまりDOMで規定されている機能については触れませんでしたが、基本的な機能は実装されています。
DOM関係の実装状況は[こちら](https://github.com/miyakogi/wdom/wiki/Features)をご参照ください。
他にも開発に便利な機能が少しあったりするのですが、それは別記事で紹介したいと思います。
