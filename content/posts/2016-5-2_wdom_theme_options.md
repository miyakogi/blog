Title: WDOMのテーマ機能と起動オプションの紹介
Slug: wdom_theme_options
Date: 2016-5-2 17:00
Category: Python
Tags: python wdom
Status: published

先日紹介したWDOMの開発者向け機能の紹介です。
CSSフレームワークを使ったテーマ機能と起動オプションについて紹介します。

基本的な機能は[前回の記事](http://h-miyako.hatenablog.com/entry/2016/04/06/185403)をご参照ください。
昨日、前回の記事に`style`属性の記述やJavaScriptを実行する方法なども追加しています。

<!--- [http://h-miyako.hatenablog.com/entry/2016/04/06/185403:embed:cite] --->

WDOMに色々更新を行ったので、ぜひ最新のバージョンでお試し下さい。
まだPyPIに登録してない＆バージョン番号をきちんと管理していないので、`pip install -U`だと更新されません。
お手数ですが一旦アンインストールしてインストールし直してください。

```
pip uinstall -y wdom && pip install git+http://github.com/miyakogi/wdom
```

前回の記事を見なおしてみると、色々夢は語っていましたが、ほとんど実現できていないですね・・・悲しい・・・
前回はテキストオンリーで寂しい感じだったので、今回は視覚に訴える感じを目指して書きます。

- [2016/05/03 追記]: デフォルトのテーマのimport方法を変更しました

<!--more-->

## テーマ機能

CSSフレームワークを使うことで見た目を自由に変更できますが、フレームワークによってボタンなどのクラス指定が異なっていて面倒です。
そこで、WDOMでは各フレームワークをラップするモジュールを提供し、手軽に見た目を変更できるようにしました。
利用可能なフレームワークは画像付きで[wiki](https://github.com/miyakogi/wdom/wiki/ScreenShots)に記載しています。
（スクリーンショットは[その道のプロ](http://selenium-python.readthedocs.io/)にお願いして一枚一枚心を込めて撮ってもらいました）

スクリーンショットは[このスクリプト](https://github.com/miyakogi/wdom/blob/dev/wdom/examples/theming.py)で要素を色々並べています。
以下の画像はBootstrapの場合です。

![bootstrap theme](https://raw.githubusercontent.com/wiki/miyakogi/wdom/images/Bootstrap3.png)

ただし、完全には各フレームワークの違いを隠蔽できていない（特にフォーム部品やGrid関係）ので、最終的にはフレームワークを決めて微調整をする必要があると思います。
また、まだ複雑なコンポーネント（タブ切り替えなど）は実装できていません・・・

数は今のところ20個ちょっとあります。
他にもよさそうなフレームワークをご存じでしたらぜひ教えてください。
ツイッターで [@miyakoDev](https://twitter.com/MiyakoDev) 宛にメンションしていただくか、[issue](https://github.com/miyakogi/wdom/issues)に登録していただければできるだけ対応します。
もちろん既存のものを参考にモジュールを書いていただいてPRを送っていただくのも大歓迎です。

ただし、ライセンスが明記されていない、あるいはGPL等の制限のあるライセンスでCDNからファイルが取得できないフレームワークは残念ながらお断りさせていただきます。
また、GPLライセンスのフレームワークでCDNから取得する場合も、最悪の場合クラス名を指定しただけでGPLの制限を受けることもないとは言い切れないので、お断りするかもしれません。
（気にしすぎだとは思いますが、わざわざリスクを犯したくないのでご理解ください）
もしこのようなフレームワークの要望があれば、別リポジトリを用意することを検討します。

### 使い方

大きく分けてふた通りあります。

一つは`from wdom.themes.フレームワーク名 import Button`などとしてモジュールから明示的にimportする方法、もうひとつは`from.wdom.themes.default import Button`などとしてimportし、起動オプションに`--theme フレームワーク名`という形で指定する方法です。

いずれの場合も、CSSやJSを読み込むためにモジュールのimport及び設定が必要になります。
また、CSSやJSは、Web上からCDN等で取得できるものはできるだけそれらを使うようにしています。
したがって、ネットに接続できない環境では利用できません。
そのような場合は、必要なファイルをローカルの適当なディレクトリに保存して、`add_static_path`でパスを追加したうえで必要なファイルを`document.add_css_file`などで読み込ませてください。

#### モジュールからimport

例えば`bootstrap3`を使う場合、以下のようになります。

```python
import asyncio
from wdom.misc import install_asyncio
from wdom.themes import bootstrap3
from wdom.themes.bootstrap3 import Button
from wdom.document import get_document
from wdom.server import get_app, start_server, stop_server

install_asyncio()
doc = get_document()
doc.register_theme(bootstrap3)

doc.body.append(Button('Click!'))
app = get_app(doc)
server = start_server(app)
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    stop_server(server)
```

`doc.register_theme(bootstrap3)`でdocumentにcssとjsを読み込む設定を行っています。
同時に、HTMLをパースした時に作られるクラスが設定されます。
例えば、`doc.createElement('button')`とするとクラス属性に`.btn`が指定された`<button>`要素（`bootstrap3.Button`クラスのインスタンス）が作られるようになり、`doc.body.innerHTML = '<button is="primary-button">PrimaryButton</button>'`とすると`bootstrap3.PrimaryButton`クラスのインスタンスが作られるようになります。

複数回`register_theme`を実行して複数のテーマを設定することも可能ですが、おそらく干渉するのでお薦めしません。
既存のフレームワーク＋自分で少しCSSを書いて追加、などは可能です。

各テーマモジュール（`wdom.themes`以下のモジュール）は`wdom.tag`クラスをimportしているので、基本的なHTMLタグに相当するクラスは全て利用可能です。

#### 起動オプションで指定

先ほどと違い、`wdom.themes.default`モジュールをimportして設定します。

```python
import asyncio
from wdom.misc import install_asyncio
from wdom.themes import default
from wdom.themes.default import Button
from wdom.document import get_document
from wdom.server import get_app, start_server, stop_server

install_asyncio()
doc = get_document()
doc.register_theme(default)

doc.body.append(Button('Click!'))
app = get_app(doc)
server = start_server(app)
try:
    asyncio.get_event_loop().run_forever()
except KeyboardInterrupt:
    stop_server(server)
```

先ほどと同様に、`doc.register_theme(default)`することで読み込むファイルやHTMLから作られるクラスが設定されます。

起動オプションに`--theme bootstrap3`と指定するとボタンが[Bootstrap](http://getbootstrap.com/)のボタンになり、`--theme pure`と指定すると[Pure](http://purecss.io/)のボタンになります。
`--theme`オプションが指定されなかったり、無効な値が指定された時はブラウザのデフォルトの表示になります。

以下の動画は上記のコードを`theme.py`として保存して、`--theme`オプションを色々変えているところです。
（端が切れているのでわかりにくいですが、実行時に`--open-browser`を指定して左側のブラウザに新しくタブを開いています）

![themes example](https://raw.githubusercontent.com/miyakogi/ss/master/wdom/themes_demo.gif)

### テーマの作り方

お気に入りのフレームワークがなかったり、既存のものに修正を加えたい場合などは作ることもできます。

[Bootstrap](https://github.com/miyakogi/wdom/blob/dev/wdom/themes/bootstrap3.py)の場合を例に簡単に作り方を紹介します。

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from wdom.tag import NewTagClass as NewTag
from wdom.tag import *

name = 'Bootstrap3'
project_url = 'http://getbootstrap.com/'
project_repository = 'https://github.com/twbs/bootstrap'
license = 'MIT License'
license_url = 'https://github.com/twbs/bootstrap/blob/master/LICENSE'

css_files = [
    '//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css',
]
js_files = [
    '//ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js',
    '//maxcdn.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap.min.js',
]
headers = []

Button = NewTag('Button', 'button', bases=Button, class_='btn')
DefaultButton = NewTag('DefaultButton', 'button', Button, class_='btn-default', is_='default-button')

（中略）

extended_classes = [
    Button,
    DefaultButton,
    ...,
]
```

まず、`from wdom.tag import *`で`wdom.tag`モジュールを全てimportします。
`from wdom.tag import NewTagClass as NewTag`として名前を変えてimportしていますが、これには特に理由はありません。
`NewTagClass`のままでも大丈夫です。
（その場合は、以下の`NewTag`を`NewTagClass`に読み替えて下さい）

そして`name = ... ~ license_url = ...`でフレームワークの情報を記入します。
これはwikiに載せるスクリーンショットを作るために使っているだけなので、自分で作ったcssなどを当てる場合は不要です。

`css_files`と`js_files`で必要なファイルを指定します。
これは指定した順番でロードされます。
上記のbootstrapの場合では`bootstrap.min.js`が`jquery`に依存しているのでそれを先に指定しています。

各要素（クラス）は`NewTag('Pythonのクラス名', '要素のタグ', 基底クラス, 任意の数の名前付き引数)`で定義します。
名前付き引数の部分は、多くの場合`class_`によるクラス属性の指定と`is_`によるis属性の指定（custom elementとしてHTMLから生成する時に使われる）だけで十分だと思います。
もちろん通常の`class`文で定義することも可能です。
クラス定義の詳細は前回の記事をご参照ください。

最後に、定義したクラスのリストを`extended_classes`に指定します。
ここで指定したクラスがHTMLからパースする時に使われます。

## 起動オプション

### ログレベル

`--logging {level}`で表示するログのレベルを指定できます。
指定可能なレベルは、詳細な順に`debug`, `info`, `warn`, `error`です。
デフォルトでは`info`に設定されます。

### ポート番号指定

デフォルトでは`8888`番ポートで起動します。
`--port 12345`などのように`--port`オプションでこのポート番号は変更できます。

適当に開いているポートを使いたい時は`--port 0`と指定してください。
毎回ポート番号が変わるとブラウザで表示を確認するのが面倒ですが、次に紹介する`--open-browser`オプションをつけると自動的にブラウザで開かれます。

### 自動ブラウザ表示

`--open-browser` オプションをつけて実行すると、実行時に自動的にブラウザのタブを開きます。
デフォルトではシステム標準のブラウザを使います。
ブラウザを指定したい場合は`--browser ブラウザ名`で指定して下さい。

Pythonの[webbrowserモジュール](http://docs.python.jp/3/library/webbrowser.html)を使っているので、指定できる名前はそちらを参照してください。
Pythonで`import webbrowser; print(webbrowser._borwsers)`とすることで利用可能な名前が確認できます。

### 自動シャットダウン

`--auto-shutdown` オプションつきで起動すると、開いているブラウザのタブが全て閉じられた時点で自動的に終了します。
タブのリロードでは終了しません。
ちょっとしたツールを作って使ってもらう時に、用が済んだらブラウザを閉じるだけで終了できます。

### 自動リロード機能

ソースファイルに変更があった時、自動的に再読み込みします。
`--autoreload` オプションをつけて起動すると有効になります。

```
python your_app.py --autoreload
```

デフォルトでは、importしているpythonのファイル、及び`add_static_path`で追加されたパス以下のファイルが監視の対象です。
これはtornadoの機能をそのまま使っています。
むしろこの機能のためにtornadoが必須ライブラリになっています。

実際に上記の3つのオプションを使ってファイルに変更を加えている様子です。

![autoreload example](https://raw.githubusercontent.com/miyakogi/ss/master/wdom/autoreload.gif)


### デバッグ

`--debug`オプションを指定することで、自動リロードが有効になりログレベルが`debug`に指定されます。
`--autoreload --logging debug`と指定した場合と同じです。

### ヘルプ

`--help`と指定するとオプションの一覧が表示されます。

## あとがき

今後書こうと思っているWDOMの紹介記事は、

* Seleniumを使ったテスト方法
* （cx_Freezeを使って）実行可能な形で配布する方法
* Electronと組み合わせて配布する方法

です。

このあたりが書き終わったらドキュメントを整備してPyPIに登録しようと思います。

他に欲しい機能とかどんなものがあるでしょうか？
パット思いつくのはJinja2やtornadoのテンプレートをパースする機能のサポートとかグラフ描画ライブラリのサポートですが。
リクエストありましたらツイッターなどで教えていただけると嬉しいです。
