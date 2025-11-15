# Cloud Run デプロイ手順ガイド

このドキュメントでは、Hatiware AI ChatアプリケーションをGoogle Cloud Platform (GCP) のCloud Runにデプロイする手順を初学者向けに説明します。

## 📚 用語解説

### 基本的な用語
- **GCP (Google Cloud Platform)**: Googleが提供するクラウドサービスのプラットフォーム
- **Cloud Run**: コンテナ化されたアプリケーションを自動でスケールさせて実行できるサーバーレスサービス
- **Docker**: アプリケーションをコンテナという独立した環境にパッケージ化する技術
- **Dockerイメージ**: アプリケーションとその実行に必要なすべての環境を含むパッケージ
- **コンテナ**: Dockerイメージから作成された実行環境
- **Artifact Registry**: Dockerイメージを保存・管理するGCPのサービス

### プロジェクト固有の用語
- **Gunicorn**: Pythonアプリケーションを本番環境で動かすためのWSGIサーバー
- **WSGI**: PythonのWebアプリケーションとWebサーバーをつなぐインターフェース規格
- **環境変数**: アプリケーションの設定をコード外部から注入する仕組み

---

## 🎯 デプロイの全体像

```
ローカル環境 → Dockerイメージ作成 → Artifact Registryに保存 → Cloud Runにデプロイ
```

---

## 📋 事前準備

### 1. GCPアカウントとプロジェクトの準備

1. **GCPアカウント作成**
   - https://cloud.google.com/ にアクセス
   - 「無料で開始」をクリック
   - Googleアカウントでログイン
   - クレジットカード情報を登録（初回は無料クレジットあり）

2. **GCPプロジェクト作成**
   - [GCPコンソール](https://console.cloud.google.com/) にアクセス
   - 画面上部の「プロジェクトを選択」→「新しいプロジェクト」をクリック
   - プロジェクト名を入力（例: `hatiware-ai-chat`）
   - 「作成」をクリック

3. **請求先アカウントの有効化**
   - プロジェクトに請求先アカウントがリンクされていることを確認
   - ナビゲーションメニュー → 「お支払い」で確認

### 2. Google Cloud CLIのインストール

**macOS の場合:**
```bash
# Homebrewを使用
brew install google-cloud-sdk
```

**Windows の場合:**
- [公式インストーラー](https://cloud.google.com/sdk/docs/install)をダウンロードして実行

**Linux の場合:**
```bash
# スナップを使用
sudo snap install google-cloud-cli --classic
```

### 3. CLIの初期設定

```bash
# Google Cloudにログイン
gcloud auth login

# デフォルトプロジェクトを設定
gcloud config set project PROJECT_ID

# ※ PROJECT_IDは先ほど作成したプロジェクトのID
# GCPコンソールで確認できます
```

### 4. 必要なAPIの有効化

```bash
# Cloud Run API
gcloud services enable run.googleapis.com

# Artifact Registry API（Dockerイメージの保存先）
gcloud services enable artifactregistry.googleapis.com

# Cloud Build API（Dockerイメージのビルド）
gcloud services enable cloudbuild.googleapis.com
```

💡 **説明**: これらのAPIを有効にすることで、GCPの各サービスが使えるようになります。

---

## 🐳 Dockerイメージの準備

### プロジェクトに既に含まれているファイル

このプロジェクトには既に以下のファイルが用意されています：

1. **Dockerfile**: アプリケーションをコンテナ化するための設計図
2. **.dockerignore**: Dockerイメージに含めないファイルを指定
3. **gunicorn.conf.py**: 本番環境用のWebサーバー設定
4. **wsgi.py**: アプリケーションのエントリーポイント

### 環境変数の準備

⚠️ **重要**: `.env`ファイルはDockerイメージに含めません！

`.env.example`を参考に、後でCloud Runの環境変数として設定します。

---

## 🚀 デプロイ手順

### 方法1: Cloud Buildを使用（推奨・簡単）

この方法では、GCPがDockerイメージのビルドから保存、デプロイまで自動で行います。

#### Step 1: デプロイコマンド実行（環境変数も同時に設定）

⚠️ **重要**: このアプリケーションは`GEMINI_API_KEY`と`MODEL_NAME`の環境変数が**必須**です。デプロイ時に必ず設定してください。

```bash
# プロジェクトのルートディレクトリで実行
# ※ YOUR_GEMINI_API_KEY を実際のAPIキーに置き換えてください
gcloud run deploy hatiware-ai-chat \
  --source . \
  --platform managed \
  --allow-unauthenticated \
  --region asia-northeast1 \
  --set-env-vars "GEMINI_API_KEY=YOUR_GEMINI_API_KEY,MODEL_NAME=gemini-2.0-flash,DEBUG_MODE=False"
```

💡 **パラメータの説明**:
- `hatiware-ai-chat`: Cloud Run サービスの名前
- `--source .`: 現在のディレクトリからビルド
- `--platform managed`: フルマネージドのCloud Runを使用
- `--allow-unauthenticated`: 認証なしでアクセス可能（公開アプリの場合）
- `--region`: デプロイするリージョン（東京: asia-northeast1、アイオワ: us-central1）
- `--set-env-vars`: 環境変数の設定（カンマ区切りで複数指定）

🔑 **Gemini APIキーの取得方法**:
1. [Google AI Studio](https://aistudio.google.com/app/apikey) にアクセス
2. 「Create API Key」をクリック
3. 表示されたAPIキーをコピーして上記コマンドの`YOUR_GEMINI_API_KEY`に貼り付け

📋 **設定可能な環境変数一覧** (.env.exampleより):

**必須設定**:
- `GEMINI_API_KEY`: Gemini APIキー（必須）
- `MODEL_NAME`: 使用するGeminiモデル（例: gemini-2.0-flash）

**任意設定**（デフォルト値あり）:
- `DEBUG_MODE`: デバッグモード（本番環境: False、開発環境: True）
- `AVATAR_NAME`: AIアシスタントの名前（デフォルト: Hatiware）
- `AVATAR_FULL_NAME`: AIアシスタントのフルネーム（デフォルト: Hatiware）
- `AVATAR_IMAGE_IDLE`: アイドル時のアバター画像（デフォルト: idle.png）
- `AVATAR_IMAGE_TALK`: 会話時のアバター画像（デフォルト: talk.png）
- `SYSTEM_INSTRUCTION`: AIの性格設定（カスタムプロンプト）
- `TYPEWRITER_DELAY_MS`: タイプライター効果の速度（デフォルト: 50）
- `MOUTH_ANIMATION_INTERVAL_MS`: 口パクアニメーション間隔（デフォルト: 150）
- `BEEP_FREQUENCY_HZ`: タイピング音の周波数（デフォルト: 800）
- `BEEP_DURATION_MS`: タイピング音の長さ（デフォルト: 50）
- `BEEP_VOLUME`: タイピング音の音量（デフォルト: 0.05）
- `BEEP_VOLUME_END`: タイピング音終了時の音量（デフォルト: 0.01）

**カスタマイズ例（ハチワレキャラクター設定）**:
```bash
gcloud run deploy hatiware-ai-chat \
  --source . \
  --platform managed \
  --allow-unauthenticated \
  --region asia-northeast1 \
  --set-env-vars "GEMINI_API_KEY=YOUR_GEMINI_API_KEY,MODEL_NAME=gemini-2.0-flash,DEBUG_MODE=False,AVATAR_NAME=Hatiware,AVATAR_FULL_NAME=Hatiware Communicator,AVATAR_IMAGE_IDLE=hatiware_close_mouth.png,AVATAR_IMAGE_TALK=hatiware_open_mouth.png,SYSTEM_INSTRUCTION=あなたは「ちいかわ」のキャラクター「ハチワレ」のように振る舞うAIアシスタントです。例：「なんとかなれッ〜！」「大丈夫だよッ、僕がついてるからッ」「〇〇..ってこと！？」「される事あるんだｱ..「触発」..」このような感じで、ハチワレらしく元気よく、ちょっと天然で、仲間想いに応答してください！よく倒置法を使って喋ります。"
```

💡 このコマンドは以下をカスタマイズしています：
- ハチワレのキャラクター性格プロンプト
- カスタムアバター画像（口を閉じた/開いた状態）
- アバター名とフルネーム

#### Step 2: デプロイ後に環境変数を変更する場合

デプロイ後に環境変数を追加・変更したい場合：

```bash
# 個別に変更
gcloud run services update hatiware-ai-chat \
  --set-env-vars "AVATAR_NAME=カスタム名" \
  --region asia-northeast1

# または、複数を一度に変更
gcloud run services update hatiware-ai-chat \
  --update-env-vars "TYPEWRITER_DELAY_MS=30,AVATAR_NAME=新しい名前" \
  --region asia-northeast1
```

💡 **--set-env-vars と --update-env-vars の違い**:
- `--set-env-vars`: 指定した環境変数を**上書き**（既存の他の環境変数は維持）
- `--update-env-vars`: 指定した環境変数のみを**更新**（推奨）

🔐 **セキュリティのヒント**: API キーなどの機密情報は、Secret Managerを使うとより安全です：

```bash
# Secret Managerにシークレットを作成
echo -n "あなたのAPIキー" | gcloud secrets create gemini-api-key --data-file=-

# Cloud RunサービスにSecret Managerから環境変数を設定
gcloud run services update hatiware-ai-chat \
  --set-secrets "GEMINI_API_KEY=gemini-api-key:latest" \
  --region asia-northeast1
```

---

### 方法2: 手動でDockerイメージをビルドしてデプロイ

より細かい制御が必要な場合は、この方法を使用します。

#### Step 1: Artifact Registryリポジトリの作成

```bash
# Dockerイメージを保存するリポジトリを作成
gcloud artifacts repositories create hatiware-repo \
  --repository-format=docker \
  --location=asia-northeast1 \
  --description="Hatiware AI Chat Docker images"
```

#### Step 2: Docker認証の設定

```bash
gcloud auth configure-docker asia-northeast1-docker.pkg.dev
```

#### Step 3: Dockerイメージのビルド

```bash
# プロジェクトIDを変数に設定
export PROJECT_ID=$(gcloud config get-value project)

# Dockerイメージをビルド
docker build -t asia-northeast1-docker.pkg.dev/$PROJECT_ID/hatiware-repo/hatiware-ai-chat:latest .
```

💡 **説明**:
- `-t`: イメージに付けるタグ（名前）
- `.`: 現在のディレクトリのDockerfileを使用

#### Step 4: イメージをArtifact Registryにプッシュ

```bash
docker push asia-northeast1-docker.pkg.dev/$PROJECT_ID/hatiware-repo/hatiware-ai-chat:latest
```

#### Step 5: Cloud Runにデプロイ（環境変数も同時に設定）

```bash
gcloud run deploy hatiware-ai-chat \
  --image asia-northeast1-docker.pkg.dev/$PROJECT_ID/hatiware-repo/hatiware-ai-chat:latest \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars "GEMINI_API_KEY=YOUR_GEMINI_API_KEY,MODEL_NAME=gemini-2.0-flash,DEBUG_MODE=False"
```

💡 `YOUR_GEMINI_API_KEY`を実際のAPIキーに置き換えてください。

#### Step 6: デプロイ後に環境変数を変更する場合

方法1のStep 2と同じ方法で環境変数を更新できます。

---

## ✅ デプロイの確認

### 1. サービスURLの確認

デプロイが完了すると、以下のようなURLが表示されます：

```
Service URL: https://hatiware-ai-chat-xxxxx-an.a.run.app
```

ブラウザでこのURLにアクセスして、アプリケーションが正常に動作しているか確認します。

### 2. ログの確認

**方法1: GCPコンソール（推奨・最も簡単）**
1. [Cloud Run コンソール](https://console.cloud.google.com/run) → `hatiware-ai-chat` → 「ログ」タブ

**方法2: CLIでリアルタイム確認**
```bash
gcloud logging tail "resource.type=cloud_run_revision AND resource.labels.service_name=hatiware-ai-chat" \
  --project=$(gcloud config get-value project)
```

**方法3: CLIで過去のログを確認**
```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=hatiware-ai-chat" \
  --limit=50 \
  --format="table(timestamp,severity,textPayload)"
```

### 3. サービス情報の確認

```bash
gcloud run services describe hatiware-ai-chat --region asia-northeast1
```

---

## 🔧 トラブルシューティング

### エラー: "Could not find Application Default Credentials"

**解決策**:
```bash
gcloud auth application-default login
```

### エラー: "Permission denied"

**解決策**:
必要なロール（Cloud Run 管理者、Artifact Registry 管理者など）が付与されているか確認
```bash
# 現在のアカウントを確認
gcloud config list account

# プロジェクトのIAMポリシーを確認
gcloud projects get-iam-policy PROJECT_ID
```

### アプリケーションが起動しない

**確認ポイント**:
1. 環境変数が正しく設定されているか
2. `GEMINI_API_KEY` が有効か
3. ログでエラーメッセージを確認

```bash
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=hatiware-ai-chat" \
  --limit=50 \
  --format="table(timestamp,severity,textPayload)"
```

### ポートのエラー

Cloud Runは環境変数 `PORT` を自動設定します。このプロジェクトの `gunicorn.conf.py` は既に対応済みです。

---

## 🔄 アプリケーションの更新

コードを変更した後、再デプロイする方法：

### 方法1を使用した場合（Cloud Build）

```bash
# 同じコマンドを再実行（環境変数も同時に設定）
gcloud run deploy hatiware-ai-chat \
  --source . \
  --platform managed \
  --region asia-northeast1 \
  --set-env-vars "GEMINI_API_KEY=YOUR_KEY,MODEL_NAME=gemini-2.0-flash,DEBUG_MODE=False"
```

💡 環境変数を変更する必要がない場合は、`--set-env-vars`を省略しても既存の環境変数は保持されます。

### 方法2を使用した場合（手動）

```bash
# Step 3〜5を再実行
export PROJECT_ID=$(gcloud config get-value project)

docker build -t asia-northeast1-docker.pkg.dev/$PROJECT_ID/hatiware-repo/hatiware-ai-chat:latest .

docker push asia-northeast1-docker.pkg.dev/$PROJECT_ID/hatiware-repo/hatiware-ai-chat:latest

gcloud run deploy hatiware-ai-chat \
  --image asia-northeast1-docker.pkg.dev/$PROJECT_ID/hatiware-repo/hatiware-ai-chat:latest \
  --platform managed \
  --region asia-northeast1
```

---

## 💰 コスト管理

### 無料枠

Cloud Runには以下の無料枠があります（2024年時点）:
- 月間200万リクエスト
- 36万vCPU秒
- 20万GiB秒のメモリ

小規模なアプリケーションなら、無料枠内で運用可能です。

### コストを抑えるヒント

1. **最小インスタンス数を0に設定**（デフォルト）
   - アクセスがない時はインスタンスが0になり、料金がかかりません
   ```bash
   gcloud run services update hatiware-ai-chat \
     --min-instances 0 \
     --region asia-northeast1
   ```

2. **CPUとメモリの制限**
   ```bash
   gcloud run services update hatiware-ai-chat \
     --cpu 1 \
     --memory 512Mi \
     --region asia-northeast1
   ```

3. **予算アラートの設定**
   - GCPコンソール → お支払い → 予算とアラート

---

## 🔒 セキュリティのベストプラクティス

### 1. Secret Managerの使用

API キーなどの機密情報はSecret Managerで管理：

```bash
# シークレットの作成
echo -n "あなたのAPIキー" | gcloud secrets create gemini-api-key --data-file=-

# Cloud Runサービスへのアクセス権を付与
gcloud secrets add-iam-policy-binding gemini-api-key \
  --member="serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/secretmanager.secretAccessor"

# サービスで使用
gcloud run services update hatiware-ai-chat \
  --set-secrets "GEMINI_API_KEY=gemini-api-key:latest" \
  --region asia-northeast1
```

### 2. 認証の追加

公開したくない場合は認証を追加：

```bash
gcloud run services update hatiware-ai-chat \
  --no-allow-unauthenticated \
  --region asia-northeast1
```

### 3. Cloud Armorの使用

DDoS攻撃や不正なアクセスを防ぐため、Cloud Armorを検討してください。

---

## 📊 モニタリングとログ

### Cloud Consoleでのモニタリング

1. [Cloud Run コンソール](https://console.cloud.google.com/run)にアクセス
2. サービス「hatiware-ai-chat」を選択
3. 「指標」タブでリクエスト数、レイテンシー、エラー率を確認

### アラートの設定

```bash
# メールでアラートを受け取る設定
# Cloud Consoleの「モニタリング」→「アラート」から設定
```

---

## 🎓 次のステップ

1. **カスタムドメインの設定**
   - Cloud Run → ドメインのマッピング
   - 独自ドメインでアクセス可能に

2. **CI/CDパイプラインの構築**
   - GitHub ActionsやCloud Buildでデプロイを自動化

3. **データベースの追加**
   - Cloud SQLやFirestoreでデータを永続化

4. **パフォーマンスの最適化**
   - Cloud CDNの利用
   - インスタンス数の調整

---

## 📚 参考リンク

- [Cloud Run 公式ドキュメント](https://cloud.google.com/run/docs)
- [Cloud Run 価格](https://cloud.google.com/run/pricing)
- [Artifact Registry ドキュメント](https://cloud.google.com/artifact-registry/docs)
- [Secret Manager ドキュメント](https://cloud.google.com/secret-manager/docs)

---

## ❓ よくある質問

### Q: デプロイにはどのくらい時間がかかりますか？
A: 初回は5〜10分程度、2回目以降は2〜3分程度です。

### Q: ローカルでDockerコンテナをテストできますか？
A: はい、以下のコマンドで可能です：
```bash
docker build -t hatiware-test .
docker run -p 5000:5000 --env-file .env hatiware-test
```

### Q: 複数の環境（本番・ステージング）を管理したい
A: サービス名を変えて複数デプロイできます：
```bash
# ステージング環境
gcloud run deploy hatiware-ai-chat-staging --source . --region asia-northeast1

# 本番環境
gcloud run deploy hatiware-ai-chat-prod --source . --region asia-northeast1
```

---

## 📝 チェックリスト

デプロイ前に確認：

- [ ] GCPプロジェクトを作成済み
- [ ] Google Cloud CLIをインストール済み（`gcloud version`で確認）
- [ ] 必要なAPIを有効化済み（run、cloudbuild、artifactregistry）
- [ ] Gemini API キーを取得済み（[Google AI Studio](https://aistudio.google.com/app/apikey)）
- [ ] `.dockerignore`に`.env`が含まれているか確認（✅ 既に設定済み）
- [ ] デプロイコマンドに環境変数を含めているか確認

デプロイ後に確認：

- [ ] アプリケーションURLにアクセスできる
- [ ] チャット機能が正常に動作する（Gemini APIと通信できているか）
- [ ] ログにエラーがないか確認（GCPコンソールの「ログ」タブ）
- [ ] 環境変数が正しく設定されているか確認
- [ ] コスト予算のアラートを設定（推奨）
- [ ] Secret Managerを使用している（本番環境では推奨）

---

以上でCloud Runへのデプロイは完了です！🎉

ご不明な点があれば、上記のトラブルシューティングセクションを確認するか、GCPのサポートにお問い合わせください。
