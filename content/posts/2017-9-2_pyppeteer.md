Title: Puppeteer (Chrome の自動操作ライブラリ) を Python に移植してpyppeteerという名前で公開しました
Slug: pyppeteer
Date: 2017-9-2 21:53
Category: python
Tags: python pyppeteer

[Puppeteer](https://github.com/GoogleChrome/puppeteer) というJavaScriptでchromeを自動操作するライブラリが最近話題になっていました。
私もPythonでSeleniumの代わりに使えるものがほしかったので、puppeteerをPythonに移植し、[pyppeteer](https://github.com/miyakogi/pyppeteer)という名前で公開しました。

<!-- more -->

Puppeteerについては下記Qiitaの投稿が参考になるかと思います。

* [--headless時代の本命？ Chrome を Node.jsから操作するライブラリ puppeteer について - Qiita](http://qiita.com/Quramy/items/26058e83e898ec2ec078)

## 使用上の注意

まだ作ったばかり＆テスト不十分なのでバグがあると思います。
なので試す時は「うまく動いたらラッキー」くらいの人柱精神でお願いします。
特にwindowsでは全くテストしていないので動かないかもしれません。

一応自分で[wdom](https://github.com/miyakogi/wdom/)の[テスト](https://github.com/miyakogi/wdom/tree/dev/tests_py36)に使ってみましたが、Webページのテストに使う分には意外と大丈夫です。
スクレイピング用途で使うとまだバグがあると思います。

バグに気づきましたら[GitHubのIssue](https://github.com/miyakogi/pyppeteer/issues)に報告していただけると幸いです。

修正してPR送っていただくのも大歓迎です。
その際は`dev`ブランチのコードを修正する形でお願いします。

## インストール

Python3.6以上のみの対応です。
pipでインストールできます。

```
python3 -m pip install pyppeteer
```

## 使い方

基本的にpuppeteerと同じです。
[puppeteerのREADME](https://github.com/GoogleChrome/puppeteer#usage)にあるWebページを開いてスクリーンショット画像を取得する例はPyppeteerでは以下のようになります。

```python
import asyncio
from pyppeteer.launcher import launch

async def main(browser):
    browser = launch()
    page = await browser.newPage()
    await page.goto('http://example.com')
    await page.screenshot({'path': 'example.png'})
    browser.close()

asyncio.get_event_loop().run_until_complete(main())
```

初回実行時だけは特定リビジョンのchrome (100MB程度) をダウンロードするので少し時間がかかります。
2回以降はすぐ終わると思います。

上記コードを実行すると同じディレクトリに`example.png`というファイルができているはずです。

APIは以下のドキュメントに列挙してあります。

* [API Reference](https://miyakogi.github.io/pyppeteer/reference.html)

`async/await`を多用しているため、かなりの数の関数/メソッドがcoroutine関数になっているので注意してください。
これらはドキュメントで名前の先頭に *coroutine* とついています。

pyppeteerのドキュメントではオプションなどについてかなり省略してしまっていますが、
puppeteerと同じになっているので必要があればpuppeteerのドキュメントを確認してください。

* https://github.com/GoogleChrome/puppeteer/blob/master/docs/api.md

また、pyppeteer自体のテストも使い方の参考になるかもしれません。

* https://github.com/miyakogi/pyppeteer/blob/master/tests/test_pyppeteer.py

上記テストで多用している`@sync`というデコレータについては下記の記事を参照してください（宣伝）。


[http://h-miyako.hatenablog.com/entry/2017/08/30/090000:embed:cite]


## Puppeteerとの違い

極力puppeteerとの違いが少ないようにしていますが、言語がJavaScriptとPythonで違う関係上多少の違いがあります。

### オプションのキーワード引数

puppeteerではオプションを辞書で設定する作りになっていますが、pyppeteerでは辞書・キーワード引数のどちらでも受け付けます。つまりPyppeteerは以下の2つの書き方が可能で、どちらも同じように動作します。

Puppeteerのように辞書で渡す:

```python
browser = launch({'headless': True})
```

キーワード引数で渡す:

```python
browser = launch(headless=True)
```

### 要素を取得するメソッド名の違い

Puppeteerでは`Page.$(selector)`というメソッドで要素を取得できますが、Pythonでは`$`が変数名に使えないので`Page.querySelector(selector)`という名前になります。
長いので`Page.J(selector)`という省略名も用意しました。

この方法で取得した要素 (`Element`) も同じように`Element.$`が使えないので`Element.querySelector`または`Element.J`となります。

同様に`$$`メソッドは`querySelectorAll`または`JJ`になります。

### `evaluate()`の引数

`Page`/`Element`の`evaluate(JSfunction)`メソッドではブラウザ上で任意のJavaScriptの関数を実行し、結果を取得することができます。

PuppeteerではJavaScriptの関数を直接引数として渡せますが、pythonではJavaScriptの関数を直接定義できませんしPythonの関数を渡しても仕方ないので、文字列で関数を渡します。

要素のテキストを取得する例は以下のようになります。

```python
element = await page.querySelector('h1')
title = await element.evaluate('(element) => element.textContent')
```

`Element.evaluate()`に渡される関数の第一引数にはその要素（上の例ではh1要素）が渡されます。
（実は`this`でも同じ要素が参照できます）

## 今後

テスト追加などで安定させ、本家puppeteerの更新に追従していこうと考えています。
機能追加についてはPython特有の機能であれば追加しますが、基本的に独自の機能は追加しないでpuppeteerとの整合性を取っていこうと考えています。

なので「こういう機能追加して！」という要望には基本的にお応えできないと思います。
puppeteerにあってこっちにない機能があれば対応しますのでお知らせください。
