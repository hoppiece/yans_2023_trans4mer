# YANS 2023 Trans4mer

YANS2023デモアプリハッカソンで作成したポスター・スライド作成支援アプリです。論文のアブストラクトからアイコンやダイアグラムを生成します。
- Promptには論文のアブストを入力してください。
- ポンチ絵に使う画像の素材が欲しい時は'icon'、ポンチ絵のレイアウト案が欲しい時は'pictogram'を選択してください。

## 環境構築

```
poetry install
```

`yans_2023_trans4mer/.env` ファイルに次の情報を準備する

```
API_ORG='' # Oranization ID
API_KEY=''
APP_PASSWORD='' # 自由に設定する
APP_USERNAME='' # 自由に設定する admin とかでいい
```
