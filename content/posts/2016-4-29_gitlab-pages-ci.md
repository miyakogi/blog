Title: GitLabでドキュメントのビルドとホスティング
Slug: gitlab-pages-ci
Date: 2016-4-29 23:8
Category: GitLab CI
Tags: gitlab mkdocs ci

完全に思いつきで、[GitLab](https://gitlab.com/)でドキュメントをgit管理してCIでビルドしてGitLab Pagesで表示する、というのをやってみました。

GitLabはGitHubみたいなサービスです。
（というかGitHubクローンで、以前はあまりにも似過ぎてたためになんか色々あったらしい、というウワサをどこかで目にしたような・・・？）
（そのせいかわかりませんが、プルリクエストはMerge Requestという名前のようですね・・・）

GitHubでも似たようなことはできますが、

- Travis CI（などのCIサービス）を使ってgh-pagesブランチにプッシュする
- Read the Docsを使ってそっちでビルド＆表示

などいずれにしろ別サービスとの連携が必要になってしまいます。
ローカルでhtmlを作って自分でpushすることもできますが、それは何か少し負けた気がするので却下です。

GitLabはCIもGitLab上で回せるので、

- リポジトリに変更をpush
- ビルドしてHTML（静的ページ）生成
- ページをホスティング

まで一つのサービスで完結できました。

GitLabのアカウントはGitHubの認証で簡単に作れるので、例えば英語ドキュメントの翻訳プロジェクトなどでは使ってみるのもありではないでしょうか。

ということで簡単に手順を紹介します。

ちなみに、思いついてからGitLabのアカウントを作るような状態でしたが、一時間足らずでリポジトリを作ってページを表示するまでできました。

- 試しに作ったリポジトリ: [https://gitlab.com/miyakogi/test-doc](https://gitlab.com/miyakogi/test-doc)
- 出力されたページ: [https://miyakogi.gitlab.io/test-doc/index.html](https://miyakogi.gitlab.io/test-doc/index.html)

<!--more-->

## リポジトリの作成

ログインして「New Project」または右上の「＋」ボタンを押せば作れます。
適当にプロジェクト名などを入力するだけです。

プロジェクトが作られたらローカルにcloneしておきます。

## ドキュメントの用意

今回は試しに[MkDocs](http://www.mkdocs.org/)を使いましたが、sphinxなどもコマンドが変わるだけで同じように使えると思います。
MkDocsはsphinxのようなドキュメントがmarkdownで書けるものです。

[GitLabのドキュメント](http://doc.gitlab.com/ee/pages/README.html#example-projects)にはJekyllや生HTML、HugoやHexoなどの例が紹介されているので、普通の静的サイトジェネレータはだいたい使えるのだと思います。
まぁHTML置くだけですからね・・・
（とはいえPythonの例が一つもないとはどういうことなんですかね・・・）

インストールは`pip install mkdocs`です。
`mkdocs new gitlab-test`でプロジェクトを作ったのですが、`gitlab-test`ディレクトリ以下に作られてしまったので`mv gitlab-test/* ./`でリポジトリのルートにファイルを全部移動させました。
このあたりはGitLabは関係ないので好みでいいと思います。

そして`index.md`を適当に編集し、`mkdocs build`でビルドすると`site`ディレクトリ以下にhtmlなどが作られます。
ローカルで確認する場合は`mkdocs serve`でhttpサーバ（tornadoっぽい）が立ち上がるので`http://localhost:8000/`にブラウザでアクセスすると表示されます。

ドキュメントが作れることを確認したら、いよいよGitLabの方の設定に入ります。

## GitLab CIの設定

リポジトリのルートに`.gitlab-ci.yml`というyaml形式の設定ファイルを作り、`git add .gitlag-ci.yml`してコミット＆プッシュすればサーバー上で実行されます。
設定ファイルは以下のようにした所うまくいきました。

```yaml
image: python: 3.5

pages:
  stage: deploy
  script:
  - pip install mkdocs
  - mkdocs build -d public
  artifacts:
    paths:
    - public
  only:
  - master
```

`image`では使用するdockerのイメージを指定するようです。
始め「デフォルトでもpipくらい使えるだろ〜」とimageを指定しなかった所、pipがなくてエラーになりました。
デフォルトでは`ruby: 2.1`のイメージが使われるようです。
apt-getでインストールすればよかったのかもしれませんが、今後使うかもしれないPythonのイメージを指定してみました。

`pages`というのがジョブの名前です。
静的ページをホストする時は`pages`という名前にする必要があるようです。
`stage: deploy`はなくてもいいかも？

`script:`以下が実際に実行されるコマンドです。
MkDocsをインストールした後にビルドしているだけですが、ここで出力先を`public`というディレクトリに指定しています。
その後に`artifacts: paths:`でパスを指定しているのでディレクトリ名は何でもいいのかと思ったのですが、デフォルトの`site`に出力して`paths`に`site`を指定してもダメでした。
ここが唯一のハマりポイントでした。
というわけで出力先は`public`に。

これをプッシュするとすぐにサーバー上でビルドが実行されます。
同一サービス上で実行されるので、GitHub + Travis CIよりやはり実行開始は早いです。
あと、`.gitlab-ci.yml`の記述がおかしいとすぐにエラーを表示してくれます。

プッシュ直後はこんな感じです。

![GitLab Top]({filename}/images/gitlab1.png)

無事にビルドできれば、`https://ユーザー名.gitlab.io/プロジェクト名`にアクセスすることでページが表示されるはずです。

## 感想

実際に使ってみてよかった点は、CIも静的ページのホスティングも単一サービスで完結しているので設定が楽、ということに尽きると思います。
思いついてから一時間足らずで完了しましたからね。
この記事書くほうが時間かかってます。
あと、無料でプライベートリポジトリも使えますし。

一方で不満だった点は、サーバーのレスポンスが（GitHubと比較して）遅い感じがするところでしょうか。
これはサーバーの立地や時間帯（日本時間金曜22時頃 = ヨーロッパの金曜昼 = アメリカ東海岸で金曜朝）のせいかもしれません。
レスポンスが悪い上にファイル一覧のUIに慣れていないので、普通の開発プロジェクトでソースコードを閲覧するのはちょっと厳しいという印象でした。

逆に、ファイルをあちこち移動しない翻訳プロジェクトなどでは候補としてありかもしれません。
MarkdownファイルをWeb上から編集して、そのままコミット→ビルドというのもできました。
もちろんコミット権限が必要ですが、権限がなくてもそのままMerge Requestが出せるのではないでしょうか（未確認）

本質的ではないのですが、いくらGitLab上でコミットしても（当然）GitHubに草が生えないのはモチベーション的に問題な気がします。
これ実はすごく深刻な問題だと思うので、GitLabさんは下克上したかったらなんとかした方がいいと思います（無茶振り）。

以上、あまりGitLabの情報を見かけなかったので思いつき＆勢いで記事にしてみました。
参考になれば幸いです。

- 参考
    - [GitLab Documentation](http://doc.gitlab.com/ee/pages/README.html)
    - [Jekyllの参考ページ](https://gitlab.com/pages/jekyll)
