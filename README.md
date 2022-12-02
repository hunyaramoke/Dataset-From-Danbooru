# Dataset-From-Danbooru
データセットをDanbooruから一括でダウンロードする為のWebUIのExtensionです。
## Note
***このソフトウェアによりダウンロードされた無断転載画像は使用しないで下さい。***  
ダウンロードされた画像を精査しpixivやtwitter等のSNSから転載されていると思われる画像は手動で削除、もしくは作者へ許可を取った上で使用してください。  
Danbooruへの負荷を避ける為、ダウンロード数は極力抑えてください。
## Installation
### Preparation
実行には予めChromeのインストール及びChromedriverのダウンロードが必要となります。  
自身のChromeのバージョンに合わせたdriverを[こちら](https://chromedriver.chromium.org/downloads)からダウンロードし、`extensions/Dataset_From_Danbooru/driver/`へ配置して下さい。
### Install
WebUI`Extensions`タブの`Install form URL`から`URL for extension's git repository`にこのリポジトリを入力しInstall
## Description
Download directory：ダウンロード先ディレクトリ（ディレクトリは事前に作成して下さい）  
Max donwloads：最大ダウンロード数  
Tag1,2：danbooruで検索するタグ。スペースは使えないので_(アンダーバー)で繋ぐこと。（例：Tag1=キャラ名, Tag2=1girl等）  
Extra tag1,2,3：Tag1,2で検索された画像に対してさらに絞りこみたい場合に使用する。  Extra tag1,2,3のいずれかがタグに含まれていれば、その画像をダウンロードする。（例：Extra tag1=fullbody, Extra tag2=school_uniform, Extra tag3=twintail等）  
Score filter：画像のスコアフィルタ。入力されたスコア以上の画像をダウンロードする。
