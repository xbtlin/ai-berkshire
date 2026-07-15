# AI Berkshire 投資哲学拡張：分析・設計・実装レポート

> 調査・実装基準日：2026-07-16 JST  
> 分析対象：[xbtlin/ai-berkshire `main@dc6c0a8bc07d9742185c26cfd8e6d96b2c9bd5fe`](https://github.com/xbtlin/ai-berkshire/tree/dc6c0a8bc07d9742185c26cfd8e6d96b2c9bd5fe)  
> 対象範囲：上記コミットの構造と検証基盤、および本作業で追加した Investor Council 機能  
> 注意：本レポートは学習・研究用であり、個別銘柄の推奨、売買指図、将来収益の保証ではない。

## 1. エグゼクティブ・サマリー

AI Berkshire の強みは、投資家の考え方を単発のプロンプトではなく、反復可能な workflow、並列 Agent、数値検証ツールに落としている点にある。一方、基準コミットでは Buffett、Munger、段永平、李録の4名が主に「担当業務」に結び付けられており、哲学の出典、適用範囲、相互矛盾を機械可読に管理する層はなかった。また、各 Agent が別々に事実を集めるため、哲学の違いではなく入力事実の違いが結論差に混入し得た。

そこで本実装では、モデルを追加学習するのではなく、次の構成を採用した。

1. 出典付きで短く言い換えた11名の投資哲学 profile
2. 研究場面と関心軸から profile を決定論的に選ぶ selector
3. 全 lens が読む一つの evidence packet
4. 独立分析、相互反証、衝突分類
5. 異なる scope の点数を平均しない統合規則

この方式なら、「誰の考え方を、どの出典から、なぜ今回使い、どの事実に適用したか」を追跡できる。哲学の出典と企業事実の出典を分離することが重要である。

```text
哲学の一次・公式・正規資料 ─→ profile registry ─→ 検証・selector ─┐
                                                           ├→ 選択済み lens
企業開示・取引所・独立資料 ─→ 共通 evidence packet ────────┘
                                     │
                                     ├→ 各 lens の独立分析
                                     ├→ 相互反証・衝突行列
                                     └→ 非平均の条件付き結論
```

併せて、基準コミットで再現した検証上の不整合も修正した。具体的には、十進計算での binary float 混入、1出典だけの「交差検証」、1出典または空の監査結果が `PASS` になる挙動、負数・ゼロの抽出欠落である。境界条件を含め、実装後は44件の自動テストが通過している。

## 2. 基準コミットの構造と強み

### 2.1 構造

基準コミットは、概ね次の三層で構成されている。

| 層 | 主な場所 | 役割 |
|---|---|---|
| Workflow / Skill | `skills/*.md` | 調査手順、出力契約、データ検証、Agent 編成を定義する canonical source |
| Agent / compatibility | `codex-skills/*/SKILL.md`、`codex-prompts/*.md` | Claude Code と Codex で同じ workflow を利用するための生成物・互換層 |
| Tool / evidence | `tools/*.py`、`data/` | 市場時価総額・評価指標・複数出典・レポート抽検などの再現可能な処理 |

これに、実例を蓄積する `reports/`、生成・インストールを担う `scripts/`、Claude 用の `CLAUDE.md` と Codex 用の `AGENTS.md` が加わる。基準コミットでは19の canonical skill があり、深度調査、決算、業界、ポートフォリオ、意思決定後の thesis 追跡まで研究ライフサイクルを広く覆っていた。

### 2.2 維持すべき強み

- **workflow first**：モデルの記憶に依存せず、同じ入口から同じ確認事項と報告構造を再現できる。
- **複数視点の対抗**：単一の「中立的」回答より、事業、財務、競争、下方リスクを別 Agent に持たせる設計は盲点発見に有効である。
- **AI の限界を明示**：情報豊富度 A/B/C、`unknown`、反対仮説、ネット接続失敗時の停止条件を workflow に含む。
- **計算を LLM から分離**：`financial_rigor.py` に数値演算を委ね、市場時価総額、評価倍率、複数シナリオを再計算できる。
- **公開前ゲート**：`report_audit.py` により、レポート中の数値を抽出し、出典値との差を検査する意図が明確である。
- **両クライアント互換**：`skills/` を正本として Codex skills / prompts を生成するため、二重保守を避けられる。

これらは作り直す対象ではなく、Investor Council が利用する土台である。

## 3. 再現した課題

### 3.1 哲学と業務分担の混同

既存の `investment-team` は、段永平を事業、Buffett を財務、Munger を業界、李録をリスク担当として割り当てる。実行上は分かりやすいが、これは各人の哲学全体ではなく業務ロールである。例えば Buffett lens は財務だけでなく、能力圏、経営者、資本配分、事業の耐久性を扱う。Munger lens も「業界担当」ではなく、逆向き思考、誘因、認知バイアス、複数モデルによる反証が中心である。

さらに、既存 workflow には「四位大师の模擬コメント」のような指示があり、公開原則を分析 lens として使うことと、本人の現在の見解を創作することの境界が曖昧になり得る。今回の skill は一人称の模倣、根拠のない引用、「本人なら買う／売る」の断定を禁止した。

### 3.2 事実差と哲学差を区別できない

既存の並列 Agent はそれぞれ Web 検索を行う。この方式は探索量を増やす一方、売上高、株式数、競争相手、時点、会計口径が Agent ごとに異なる可能性がある。その場合、結論の衝突が哲学によるものか、単に入力データが違うためか判定できない。

Investor Council では、最初に一つの evidence packet を作り、全 lens に同じ packet と同じ URL 一覧を渡す。新しい事実が質疑中に見つかった場合も、個別レポートへ直接足さず、二重出典確認後に packet へ戻す。

### 3.3 異質な評価の平均

会社の質、証券価格、ポートフォリオ適合性、投資家行動は別の問いである。Bogle lens に個別企業の moat を採点させたり、Dalio lens の環境耐性と Fisher lens の研究開発評価を星の平均にしたりすると、意味のない精密さが生じる。基準コミットの総合点は比較の利便性があるが、適用 scope が異なる哲学の追加後は、そのまま拡張できない。

### 3.4 検証基盤で実際に再現した不整合

以下は 2026-07-16 JST に、`git show "dc6c0a8:{path}" | python3 - ...` という形で基準コミットのコードを直接実行して再現した結果である。

| 再現項目 | 基準コミットの結果 | 問題 |
|---|---|---|
| `calc --expr '0.1 + 0.2'` | 「精確値」`0.30000000000000004`、終了コード0 | Python の `float` で評価した後に `Decimal` 化しており、「最初から十進法」という説明と不一致 |
| `cross-validate` に `{"only-source": 100}` だけを渡す | 「全出典一致」、既定許容差2%、終了コード0 | 交差検証なのに2出典を強制せず、リポジトリ規則の1%とも不一致 |
| `report_audit verdict` に一致する1出典だけを渡す | `PASS`、終了コード0 | workflow が要求する独立2出典を実装が強制していない |
| `report_audit verdict --results '[]'` | `PASS`、終了コード0 | 何も検査していないレポートが公開可能になる fail-open |
| `-12.5億`、`0億元`、`−3.2%` を抽出 | `-12.5億` を正の `12.5` と誤認し、ゼロと Unicode minus の値を欠落 | 損失・ゼロという重要な財務状態が標本から消える |

このため、既存レポート群は有用な研究例ではあるが、過去に `PASS` したことだけを正解ラベルや将来予測力の証拠として扱うべきではない。

## 4. なぜ fine-tuning ではないのか

今回必要なのは文章の口調ではなく、出典、適用範囲、更新可能性、相互反証である。fine-tuning を中核にすると、次の問題が残る。

| 要件 | Fine-tuning の弱点 | profile + selector + evidence + 討論の利点 |
|---|---|---|
| 出典追跡 | どの学習文がどの出力に効いたか説明しにくい | 各 profile に URL と source kind を保持できる |
| 更新 | 新しい書簡、memo、公式方針を反映するたび再学習が必要 | JSON の profile と `reviewed_at` を更新すればよい |
| 事実の鮮度 | モデル重みに現在の価格・決算を固定すべきでない | 最新事実を毎回 evidence packet として投入する |
| 哲学間の矛盾 | 一つのモデル重みの中で平均化・混合しやすい | lens ごとに独立出力し、衝突を残せる |
| 著作権・帰属 | 書籍全文や有料資料を学習集合へ入れるリスク | 短い独自要約と公式・出版元リンクだけを保持する |
| 誤った本人性 | 文体模倣が「本人の意見」に見えやすい | 常に「公開資料に着想を得た lens」と明記する |
| 監査・テスト | 挙動の理由を unit test にしにくい | schema、選択順、拒否条件、出力契約をテストできる |

将来 fine-tuning を使う余地はあるが、用途は schema に沿った整形、ラベル付け、長文圧縮などに限定すべきである。哲学の事実源や最新企業データの保存先にはしない。

## 5. 11名の lens と主要資料

registry は「本人そのもの」ではなく、公開資料から独自に短く言い換えた質問セットである。本人資料の `primary` / `primary_platform`、本人の所属組織による `official_firm`、資料保存主体による `official_archive` / `institutional_archive`、正規 `publisher` の6種を区別する。主要な役割と参照先は以下の通りである。

| Lens | 評議会での主な役割 | 主な一次・公式・正規資料 |
|---|---|---|
| Warren Buffett | 企業所有者の視点、moat、経営者、資本配分、内在価値と集中の条件 | [Berkshire shareholder letters](https://www.berkshirehathaway.com/letters/letters.html)、[Owner's Manual](https://www.berkshirehathaway.com/owners.html)（一次） |
| Charlie Munger | 逆向き思考、誘因、認知バイアス、失敗経路、学際モデル | [Berkshire 2023 Annual Report の追悼資料](https://www.berkshirehathaway.com/2023ar/2023ar.pdf)（公式企業）、[Poor Charlie's Almanack](https://www.stripe.press/poor-charlies-almanack)（正規出版元） |
| 段永平 | 事業モデル、差別化、企業文化、能力圏、やらないこと | [公開雪球アカウント](https://xueqiu.com/u/1247347556)（本人の公開 platform。投稿時点と文脈の確認が必須） |
| 李録 | 長期確実性、信頼できる経営、moat、永久損失、知らないことの明示 | [Himalaya Capital: What We Do / Investment Philosophy / Core Values](https://www.himcap.com/)（公式企業） |
| Benjamin Graham | 保守的内在価値、財務安全性、安全余裕、規律、分散 | [Columbia Business School: History of Value Investing](https://business.columbia.edu/heilbrunn/about/valueinvestinghistory)、[CFA Institute Research Foundation archive](https://rpc.cfainstitute.org/research/foundation/1977/benjamin-graham-the-father-of-financial-analysis-full-pdf)（機関アーカイブ） |
| Philip Fisher | 長い成長余地、研究開発・販売・組織力、外部公開情報による裏取り | [Wiley: Common Stocks and Uncommon Profits and Other Writings](https://www.wiley-vch.de/en/areas-interest/finance-economics-law/finance-investments-13fi/investments-securities-13fi3/common-stocks-and-uncommon-profits-and-other-writings-978-0-471-44550-0)（正規出版元） |
| Peter Lynch | 日常観察からの候補発見、企業分類、分かりやすい利益 driver、財務耐久性 | [Fidelity: Peter Lynch / Chris Kuiper interview transcript](https://www.fidelity.com/bin-public/060_www_fidelity_com/documents/learning-center/110322%20rewards%20exclusive_UnderstandtheChange-Transcript_%20F.pdf)（本人発言の公式 transcript）、[Simon & Schuster: One Up On Wall Street](https://www.simonandschuster.com/books/One-Up-On-Wall-Street/Peter-Lynch/9780743200400)（正規出版元） |
| Howard Marks | 価格に織り込まれた期待、二次的思考、cycle、信用、損失分布 | [Oaktree: The Best of Howard Marks's memos](https://www.oaktreecapital.com/insights/memo/the-best-of)、[You Can't Predict. You Can Prepare.](https://www.oaktreecapital.com/docs/default-source/memos/2001-11-20-you-cant-predict-you-can-prepare.pdf)（一次 memo） |
| John Bogle | 低コスト指数という反証基準、分散、費用・税・行動 drag | [Bogle Archive](https://boglecenter.net/bogle-archive/)（非営利団体による機関アーカイブ）、[Vanguard history](https://corporate.vanguard.com/content/corporatesite/us/en/corp/why-vanguard/who-we-are/our-history.html)（公式企業） |
| Ray Dalio / Bridgewater | 成長・インフレ環境、リスク寄与、相関変化、組合せの stress test | [Bridgewater: The All Weather Story](https://www.bridgewater.com/research-and-insights/the-all-weather-story)（公式企業）、[Principles](https://www.principles.com/principles/)（本人公式） |
| Joel Greenblatt | 品質と価格の二軸 ranking、ルール実行、分散、special situation | [Gotham Funds: Investment Strategy](https://www.gothamfunds.com/strategy)、[Magic Formula Investing: How It Works](https://www.magicformulainvesting.com/Home/HowItWorks)（公式企業）、[Simon & Schuster: You Can Be a Stock Market Genius](https://www.simonandschuster.com/books/You-Can-Be-a-Stock-Market-Genius/Joel-Greenblatt/9780684840079)（正規出版元） |

この一覧は網羅的 canon ではない。特に出版元・機関アーカイブは本人の一次資料と同じ強さではなく、`sources[].kind` にその差を残す。長い原文リストを複製せず、実際の分析では各リンクを開いて文脈を確認する。

## 6. 哲学間の矛盾と「平均しない」統合規則

拡張の価値は、11人を同意させることではなく、同じ事実から生じる本物の緊張を保存することにある。

| 衝突 | 一方の問い | 他方の問い | 裁決に必要なもの |
|---|---|---|---|
| 集中 vs 分散 | Buffett / 李録：高確度の希少機会へ大きく配分できるか | Graham / Bogle / Greenblatt：単一判断の誤りをどう吸収するか | ユーザーの損失許容度、資金需要、優位性の実証 |
| 良い会社 vs 安い証券 | Fisher / Buffett：長い再投資 runway と質はあるか | Graham / Marks / Greenblatt：期待を含む価格に安全余裕があるか | 価格時点、逆算成長率、下方シナリオ |
| アクティブ選択 vs 市場全体保有 | Lynch / Fisher：調査可能な個別優位があるか | Bogle：費用・税引後で低コスト指数に勝つ根拠があるか | point-in-time 比較、費用、税、継続可能性 |
| bottom-up vs macro regime | Buffett / 段永平：理解できる事業と価値に集中する | Dalio / Marks：成長、インフレ、信用・心理 cycle への曝露は何か | 予言ではなく複数環境の stress test |
| 定性文化 vs 定量規則 | 段永平 / 李録 / Munger：文化、誠実さ、誘因はどうか | Greenblatt / Graham：再現可能な数値条件を満たすか | 定性証拠を別欄に保持し、screen と最終判断を分離 |

統合は次の順序で行う。

1. **scope gate**：`company`、`security`、`portfolio`、`behavior` のどれを答えているか確認する。範囲外は `N/A`、範囲内だが証拠不足は `unknown` とし、どちらも0点にしない。
2. **evidence gate**：重要数値の二重出典、時点、通貨、口径が揃わなければ先へ進めない。
3. **hard veto**：重大な不正、支払不能、違法性、経営者の信頼性崩壊、重要データ検証不能などは、平均点で相殺しない。
4. **robust consensus**：異なる哲学と仮定でも残る結論だけを「頑健な共通認識」とする。
5. **conflict preservation**：衝突を、事実、時間軸、評価、リスク定義、scope、ユーザー条件のどれかに分類し、解消に必要な新証拠を書く。
6. **conditional conclusion**：価格、事実、投資期間、損失許容度がどう変われば結論が変わるかを示す。
7. **baseline comparison**：個別能動案には、低コスト指数の費用・税引後ケースを併記する。

出力は「頑健な共通認識」「主要な衝突」「hard veto」「条件付き結論」「基準比較」「残余 unknown」であり、星や百分率の総平均ではない。

## 7. 実装内容

### 7.1 出典付き profile registry

[`data/investor_philosophies.json`](../data/investor_philosophies.json) を追加した。`schema_version=1`、レビュー日、30の focus tag、7 scenario、11 investor、20 source URL を持つ。各 investor には以下を必須化している。

- 安定した `id`、表示名、学派、適用 scope
- 独自の短い要約、原則、研究時の問い
- `focus_tags`、得意用途、限界
- HTTPS の source URL と source kind

保存するのは独自の短い言い換えとリンクであり、書籍本文、長い checklist、有料 memo の複製ではない。

### 7.2 決定論的 selector / CLI

[`tools/investor_council.py`](../tools/investor_council.py) を追加した。外部依存のない Python CLI で、次を行う。

- `validate`：schema、重複 ID、scope、tag、scenario default、HTTPS URL、source kind を一括検証
- `list` / `show`：利用可能な lens と profile を確認
- `select`：scenario default、focus tag、明示 ID から最大6 lens を選択
- `markdown` / `json` / `ids`：Agent、文書、script から再利用できる出力

追加 focus がない場合は scenario の既定順を保つ。focus がある場合は、まずユーザー指定 tag を上限内で最大限カバーし、その後に scenario 適合、学派の多様性、未カバー tag の増分を使って決定論的に残りを選ぶ。上限のため指定 tag を全てカバーできない場合は `uncovered_focus_tags` に記録し、Markdown は本文内、JSON / ids は標準エラーに警告を出す。ユーザーが明示した lens は順序を保存し、不明な scenario、tag、lens、上限違反は非0で終了する。これは銘柄を採点する道具ではなく、分析に使う問いを選ぶ道具である。

7 scenario は `company`、`growth`、`deep-value`、`china-quality`、`portfolio`、`special-situations`、`active-vs-passive` である。例えば `company` の既定評議会は Buffett、Munger、Fisher、Marks となる。

### 7.3 canonical skill

[`skills/investor-council.md`](../skills/investor-council.md) を追加した。主な契約は次の通りである。

- 実行前に日付、registry、selector を検証する。
- lens を事前登録し、結論を見た後で都合の良い投資家へ差し替えない。
- 全 lens が同じ evidence packet を読む。
- 各 lens は適用性、最大3結論、対応証拠、unknown、最強反証、hard veto、結論変更条件、信頼度、哲学 URL を同じ schema で返す。
- 最大4 Agent を同時実行し、一巡の相互反証を行う。
- 本人の一人称、架空の引用、現在の売買意向、endorsement を生成しない。
- 財務データは既存の厳密計算と report audit を通す。
- 既存互換方針に従い、canonical skill から Codex skill / prompt を生成する。

同期 script により [`codex-skills/investor-council/SKILL.md`](../codex-skills/investor-council/SKILL.md) と [`codex-prompts/investor-council.md`](../codex-prompts/investor-council.md) も生成した。これらは派生物であり、変更の正本は引き続き `skills/investor-council.md` である。

同期チェックを厳格な回帰条件にしたため、基準コミット時点で canonical source とずれていた `codex-skills/deep-company-series/SKILL.md`、`codex-skills/investment-team/SKILL.md`、`codex-prompts/deep-company-series.md` も、既存の同期 script の出力に合わせて更新した。これらに新しい哲学判断を手作業で加えたものではない。

### 7.4 検証基盤の修正

[`tools/financial_rigor.py`](../tools/financial_rigor.py) では、CLI の数値を文字列から `Decimal` として読み、四則演算を制限付き AST で評価するようにした。`eval` と binary float を計算入口から外し、`0.1 + 0.2` は `Decimal('0.3')` になる。Python 3.7 の `ast.Num` と新しい `ast.Constant` の双方を安全に扱い、ゼロ価格や負の予測年数も traceback ではなく制御された非0終了にする。`cross-validate` は2つ以上の名称の異なる出典、有限値、既定1%を要求し、中央値からの距離ではなく全出典間の全ペア相対差で合否を決める。不一致や無効入力、市場時価総額の重大不一致は非0終了へ反映する。

[`tools/report_audit.py`](../tools/report_audit.py) では、空結果、未検証値、第二出典欠落、同名出典、どちらか一方の1%超過をすべて `FAIL` にした。`unknown`、`TBD`、`未検証` 等の placeholder も出典名として受理しない。二つの独立した出典がともに1%以内の場合だけ `PASS` する。負数、Unicode minus、ゼロを抽出対象に含め、Markdown 表の内部空セルを保持して年度列のずれを防ぎ、比較を `Decimal` 化した。`--output-json` は標準出力を純粋な JSON に保ち、CLI の終了コードを判定と一致させた。

ここでいう「独立」は現段階では正規化した出典名が異なることまでである。同じデータ vendor を別名で記入することや、同一企業グループ内の再配信を完全には検出しないため、domain・原資料 ID による強化が今後必要である。

### 7.5 自動テスト

以下を追加した。

- [`tests/test_investor_council.py`](../tests/test_investor_council.py)：registry、source URL、scenario default、focus 選択、明示順、異常系、非 endorsement 文言、skill 契約
- [`tests/test_financial_rigor.py`](../tests/test_financial_rigor.py)：十進演算、科学表記、Python 3.7 AST 互換、`eval` 不使用、四則以外の拒否、全ペア1%境界、2出典、ゼロ除算、CLI 終了コード
- [`tests/test_report_audit.py`](../tests/test_report_audit.py)：負数・ゼロ・内部空セル抽出、空・placeholder・第二出典欠落・同一出典・片側不一致の拒否、正常な二重検証、純粋 JSON 出力、CLI 終了コード
- [`tests/test_generated_artifacts.py`](../tests/test_generated_artifacts.py)：全 canonical skill の Codex skill / prompt 対応、生成物の同期状態、README の skill 数

2026-07-16 JST の確認結果は次の通りである。

```text
python3 -m unittest discover -s tests -v
Ran 44 tests ... OK

python3 tools/investor_council.py validate
哲学レジストリは有効：11 investor / 7 scenario / reviewed_at 2026-07-16

python3 scripts/sync-codex-skills.py --check
20 Codex skills checked

python3 scripts/sync-codex-prompts.py --check
20 Codex prompts checked
```

## 8. 使い方

### 8.1 registry と selector の確認

```bash
python3 tools/investor_council.py validate
python3 tools/investor_council.py list
python3 tools/investor_council.py show howard-marks
```

会社研究の既定4 lens を Markdown で出す。

```bash
python3 tools/investor_council.py select \
  --scenario company \
  --limit 4 \
  --format markdown
```

ポートフォリオを費用・経済環境まで含めて選ぶ。

```bash
python3 tools/investor_council.py select \
  --scenario portfolio \
  --focus costs,regime \
  --limit 4 \
  --format json
```

比較したい lens を明示する。

```bash
python3 tools/investor_council.py select \
  --scenario active-vs-passive \
  --lenses john-bogle,warren-buffett,howard-marks \
  --limit 3 \
  --format ids
```

### 8.2 Skill からの研究

Claude Code の slash-command または Codex skill では、例えば次の入力を使う。

```text
/investor-council NVIDIA | scenario=growth | lenses=auto | focus=innovation,valuation,risk | max=4
```

実行時には、selector の出力だけで結論を出さず、対象企業について一つの evidence packet を先に作る。少なくとも時点・通貨・株式数・時価総額、5年と直近4四半期の財務、segment economics、競争、経営者と資本配分、評価、強気・弱気仮説、unknown を含める。重要数値は会社開示または取引所を含む二つの独立出典で検証する。

### 8.3 公開前の最小確認

```bash
python3 -m unittest discover -s tests -v
python3 scripts/sync-codex-skills.py --check
python3 scripts/sync-codex-prompts.py --check

python3 tools/report_audit.py extract \
  --report 'reports/{対象}/{report}.md' \
  --seed 42

python3 tools/report_audit.py verdict \
  --results '<二つの独立出典を記入したJSON>' \
  --report '<report>.md'
```

`PASS` は抽出標本の数値が条件を満たしたことを示すだけで、投資 thesis、source の意味上の独立性、将来リターンの正しさまでは証明しない。

## 9. 限界とロードマップ

### 9.1 現在の限界

- **profile は編集判断を含む**：30 tag、要約、質問、scenario default は機械的真理ではない。`reviewed_at` と変更理由の記録が必要である。
- **URL 検証は構文中心**：CLI は HTTPS、必須項目、重複を検査するが、リンク先の意味、改訂、redirect、page 消失を保証しない。
- **公開原則は現在の本人見解ではない**：lens の出力を本人の推奨、承認、実際の保有判断と解釈できない。
- **共通 packet も誤り得る**：同じ誤った事実を全 Agent に配れば、整然と同じ誤答になる。共通化は二重出典を代替しない。
- **selector は単純な heuristic**：安定・監査可能である一方、予測精度を最適化したものではない。
- **独立出典判定は浅い**：現在は名称の一致を拒否する段階で、domain、原 filing、データ系列の同源性までは判定しない。
- **網羅性と代表性**：11名は価値・品質・成長・cycle・passive・macro・systematic を広げるが、地域、時代、資産 class、投資家属性の代表として十分ではない。
- **実証未完了**：複数 lens が単一 lens より良い投資成果を生むという backtest や前向き評価はまだない。
- **個人適合性は別問題**：税制、法域、収入、負債、流動性需要、損失許容度を入力しない限り、portfolio の結論は一般論に留まる。

### 9.2 推奨ロードマップ

**優先度 P0 — 監査可能性**

1. evidence packet を claim ID、期間、通貨、単位、原 URL、取得時刻、source independence key を持つ JSON schema にする。
2. 哲学 source の定期 link check、content fingerprint、差分 review を CI 化する。
3. `report_audit` の独立性を出典名から registrable domain、原 filing ID、企業グループまで拡張する。
4. selector の入力、registry version、選択結果、最終衝突行列を report artifact として保存する。

**優先度 P1 — 品質評価**

1. point-in-time データだけを使う過去時点 replay と、将来情報混入を防ぐ benchmark を作る。
2. 単一 lens、複数 lens、討論なし、共通 packet なしの ablation を行い、どの構成が誤りを減らすか測る。
3. 結論の的中だけでなく、出典充足率、unknown の正直さ、反証発見率、同じ入力での安定性を評価する。
4. 既存の `investment-team` / `investment-research` から共通 evidence packet と非平均規則を再利用できるよう統合する。

**優先度 P2 — 拡張**

1. 地域・資産 class・投資手法の偏りを点検し、同じ source quality 条件で lens を追加する。
2. 日本語・中国語・英語の原資料を別々に保持し、翻訳文と原文の対応を claim 単位で示す。
3. special situations、credit、private company などに専用の衝突 template を用意する。
4. 必要なら検索・整形に embeddings や fine-tuning を使うが、出典 registry と最新 evidence は外部の監査可能な形に残す。

## 10. 著作権、帰属、免責

- profile の本文は公開資料を基にした独自の短い要約であり、本人の発言を長く逐語引用していない。原典を確認できるようリンクを近接配置した。
- Fisher の checklist、書籍章、Oaktree memo、その他の著作物を元の順序で大量複製しない。引用が必要な場合も最小限とし、出典、文脈、翻訳である旨を明示する。
- Investor 名は分析 lens の識別に使用しているだけで、本人、遺族、所属企業、出版社が本プロジェクトに参加・承認・推薦したことを意味しない。
- リポジトリの MIT License は本プロジェクト自身の code / documentation に適用される。リンク先の書籍、memo、Web page、商標等の権利を再許諾するものではない。
- 分析結果は入力データ、時点、会計口径、モデル仮定に依存する。価格、為替、税制、規制、企業状況は変化する。過去の実績や backtest は将来の成果を保証しない。
- 本機能は教育・研究支援であり、投資助言、適合性判定、法務・税務助言、売買執行ではない。利用者は原資料を確認し、自身の状況に応じて独立に判断する必要がある。

## 結論

AI Berkshire を「著名投資家を演じる AI」へ広げるべきではない。広げるべきなのは、出典が見える問いの集合、同じ事実に対する異なる推論、反証可能な衝突、そして不明を不明のまま残す規律である。本実装の11名 registry、決定論的 selector、共通 evidence packet、討論、非平均統合は、そのための最小で監査可能な基盤である。
