# Skill-Squared

Claude Code スキルを管理・メンテナンスするためのメタスキル - プロジェクトの作成、コマンドの追加、マーケットプレイスへの同期、構造の検証。

## インストール

Claude Code で、まずマーケットプレイスを登録します：

```bash
/plugin marketplace add syfyufei/skill-squared
```

次に、このマーケットプレイスからプラグインをインストールします：

```bash
/plugin install skill-squared@skill-squared-marketplace
```

### インストールの確認

コマンドが表示されることを確認します：

```bash
/help
```

```
# 4つのコマンドが表示されます：
# /skill-squared:create - 新しいスキルプロジェクト構造を作成
# /skill-squared:command - 既存のスキルにスラッシュコマンドを追加
# /skill-squared:sync - スタンドアロンリポジトリからマーケットプレイスへスキルを同期
# /skill-squared:validate - スキルの構造と設定を検証
```

## 使用方法

### 新しいスキルの作成

必要なファイルをすべて含む完全なスキルプロジェクトを作成：

```bash
/skill-squared:create
```

または自然言語を使用：
```
"data-analyzerという新しいスキルを作成"
```

### コマンドの追加

既存のスキルに新しいスラッシュコマンドを追加：

```bash
/skill-squared:command
```

または自然言語を使用：
```
"自分のスキルにprocess-dataというコマンドを追加"
```

### マーケットプレイスへの同期

スタンドアロンリポジトリからマーケットプレイスへスキルを同期：

```bash
/skill-squared:sync
```

または自然言語を使用：
```
"data-analyzerスキルをadrian-marketplaceに同期"
```

### スキルの検証

スキルの構造と設定を検証：

```bash
/skill-squared:validate
```

または自然言語を使用：
```
"スキルの構造を検証"
```

## 機能

- **完全なプロジェクト生成**：テンプレートを使用して完全に設定されたスキルプロジェクトを作成
- **コマンド管理**：スラッシュコマンドの簡単な作成と登録
- **マーケットプレイス同期**：マーケットプレイスリポジトリへのスキル同期
- **検証**：包括的な構造と設定の検証
- **テンプレートシステム**：変数置換によるカスタマイズ可能なテンプレート
- **デュアルリポジトリパターン**：スタンドアロン開発 + マーケットプレイス配布

## アーキテクチャ

Skill-Squaredは**デュアルリポジトリパターン**に従います：

### スタンドアロンリポジトリ（開発）
- 完全なスキル実装
- 独立したバージョン管理
- 自己完結型インストール
- 開発とテスト

### マーケットプレイスリポジトリ（配布）
- 複数のスキルを集約
- skill.mdとコマンドのみをコピー
- ユーザー向けワンストップインストール
- スタンドアロンリポジトリから同期

## ワークフロー

1. **作成**：`/skill-squared:create`
2. **カスタマイズ**：`skills/{skill-name}.md`のスキルロジック
3. **コマンド追加**：`/skill-squared:command`
4. **検証**：`/skill-squared:validate`
5. **インストールテスト**：`cd skill-name && ./install.sh`
6. **同期**：`/skill-squared:sync`
7. **コミット**して両方のリポジトリをプッシュ

## ドキュメント

- **[コマンドリファレンス](./docs/commands-reference.md)** - 完全なコマンドドキュメント
- **[テンプレートガイド](./docs/template-guide.md)** - テンプレートのカスタマイズ
- **[ベストプラクティス](./docs/best-practices.md)** - スキル開発ガイドライン

## 設定

Skill-Squaredは`config/config.json`を使用：
- 検証ルール（必須ファイル、フロントマターフィールド）
- 同期設定（バックアップ、同期するファイル）
- テンプレートパスと変数
- デフォルト値

## ライセンス

MITライセンス - 詳細は[LICENSE](./LICENSE)を参照

---

**バージョン**：0.1.0
**作者**：Adrian <syfyufei@gmail.com>
**リポジトリ**：https://github.com/syfyufei/skill-squared

*スキルを開発するためのスキル*
