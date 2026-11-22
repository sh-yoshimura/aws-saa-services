## しくみ

オンプレミスと VPC を、**インターネット上の暗号化された IPsec トンネル**でつなぎます。

- AWS 側：**仮想プライベートゲートウェイ（VGW）**（VPC にアタッチ）か [[transit-gateway]]
- オンプレミス側：**カスタマーゲートウェイ**（ルーターなどの機器の情報を AWS に登録する）
- 1 つの VPN 接続に **2 本のトンネル**があり、冗長化されている
- 1 トンネルあたりの帯域は最大 1.25 Gbps 程度。Transit Gateway の ECMP で束ねると増やせる
- **Accelerated VPN**：[[global-accelerator]] のネットワークを通して、安定性を高める

## Direct Connect との比較

| 項目 | Site-to-Site VPN | [[direct-connect]] |
|---|---|---|
| 経路 | インターネット | 専用線 |
| 暗号化 | あり（IPsec） | 標準ではなし |
| 開通 | **数分〜数時間** | 数週間〜数か月 |
| 帯域の安定性 | インターネットに左右される | 安定 |
| コスト | 低い | 高い |

## 関連する VPN

- **AWS Client VPN**：個人の PC から VPC へ接続する（リモートワーク用）
- **VPN CloudHub**：複数の拠点を 1 つの VGW につないで、拠点同士も通信できるようにする

## 試験でのポイント

- 「すぐに」「低コストで」「暗号化して」オンプレミスとつなぐ → Site-to-Site VPN
- Direct Connect の**バックアップ回線**として頻出

## よくあるひっかけ

- 社員の PC から接続する話なら Site-to-Site VPN ではなく **Client VPN**
