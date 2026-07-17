"""Japanese presentation layer for Investor Council API structures.

The canonical philosophy registry remains language-neutral infrastructure owned by
the research workflow.  This module provides a pure, fail-closed localization
boundary for the Japanese web UI: every public function returns a deep copy and
never mutates its input.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Final, Mapping, TypedDict


JsonObject = dict[str, Any]

__all__ = [
    "FOCUS_TAXONOMY_JA",
    "INVESTOR_TRANSLATIONS_JA",
    "LocalizationError",
    "SCENARIO_DESCRIPTIONS_JA",
    "SCHOOL_LABELS_JA",
    "SCOPE_LABELS_JA",
    "SELECTION_MODE_LABELS_JA",
    "SOURCE_KIND_LABELS_JA",
    "localize_catalog",
    "localize_profile",
    "localize_selection",
]


class LocalizationError(ValueError):
    """Raised when an API structure cannot be localized completely and safely."""


class InvestorTranslation(TypedDict):
    """Complete Japanese copy for one investor philosophy profile."""

    name_ja: str
    school_ja: str
    summary: str
    principles: tuple[str, ...]
    questions: tuple[str, ...]
    best_for: tuple[str, ...]
    limitations: tuple[str, ...]


FOCUS_TAXONOMY_JA: Final[dict[str, str]] = {
    "asset_allocation": "資産配分",
    "asset_value": "資産価値",
    "behavior": "投資家行動・心理",
    "business_quality": "事業の質",
    "capital_allocation": "資本配分",
    "catalyst": "価値実現のカタリスト",
    "circle_of_competence": "能力の輪",
    "consumer_observation": "消費者・日常観察",
    "costs": "コスト・税負担",
    "credit": "信用・資金調達環境",
    "culture": "企業文化",
    "cycle": "市場・信用サイクル",
    "diversification": "分散",
    "downside": "恒久的損失・下方リスク",
    "growth": "長期成長",
    "innovation": "イノベーション・研究開発",
    "macro": "マクロ環境",
    "management": "経営陣の質",
    "margin_of_safety": "安全域",
    "moat": "競争優位・経済的な堀",
    "opportunity_cost": "機会費用",
    "passive": "パッシブ投資の基準",
    "portfolio": "ポートフォリオ構築",
    "quantitative": "定量スクリーニング",
    "regime": "経済環境への適応力",
    "research_network": "外部情報による事実検証",
    "risk": "リスクの特定・管理",
    "special_situations": "特殊状況",
    "systematic": "ルールに基づく実行",
    "valuation": "バリュエーション",
}


SCENARIO_DESCRIPTIONS_JA: Final[dict[str, str]] = {
    "company": "上場企業1社の事業の質・価格・リスクを調査",
    "growth": "成長企業と、その成長の質を調査",
    "deep-value": "低評価、資産価値からの乖離、安全域を調査",
    "china-quality": "中国企業のビジネスモデル・文化・長期的な確実性を調査",
    "portfolio": "資産配分・コスト・分散と、経済環境別の耐性を検証",
    "special-situations": "スピンオフ・再編・イベントドリブン・複雑な証券を調査",
    "active-vs-passive": "アクティブな銘柄選択と低コスト指数の基準を比較",
}


SCOPE_LABELS_JA: Final[dict[str, str]] = {
    "company": "企業",
    "security": "証券",
    "portfolio": "ポートフォリオ",
    "behavior": "投資家行動",
}


SOURCE_KIND_LABELS_JA: Final[dict[str, str]] = {
    "primary": "一次資料",
    "primary_platform": "本人の公式発信基盤",
    "official_firm": "企業・運用会社の公式資料",
    "official_archive": "公式アーカイブ",
    "institutional_archive": "機関アーカイブ",
    "publisher": "出版社",
}


SCHOOL_LABELS_JA: Final[dict[str, str]] = {
    "quality-value": "クオリティ・バリュー",
    "multidisciplinary-inversion": "学際的思考・逆算",
    "business-model-culture": "ビジネスモデル・企業文化",
    "defensive-value": "防御的バリュー",
    "quality-growth": "クオリティ・グロース",
    "researchable-growth": "調査重視の成長株投資",
    "cycle-risk": "サイクル・リスク",
    "low-cost-indexing": "低コスト・インデックス",
    "macro-risk-balance": "マクロ・リスクバランス",
    "systematic-value": "システマティック・バリュー",
}


SELECTION_MODE_LABELS_JA: Final[dict[str, str]] = {
    "explicit": "指定したレンズ",
    "scenario-default": "シナリオの標準構成",
    "focus-ranked": "関心軸に基づく選定",
}


INVESTOR_TRANSLATIONS_JA: Final[dict[str, InvestorTranslation]] = {
    "warren-buffett": {
        "name_ja": "ウォーレン・バフェット",
        "school_ja": "クオリティ・バリュー",
        "summary": (
            "株式を企業の所有権と捉え、能力の輪の中で、持続的な競争優位、"
            "信頼できる経営陣、長期的な再投資余地を備えた企業を探し、"
            "内在価値に比べて魅力的な価格で買う。"
        ),
        "principles": (
            "証券価格を論じる前に、その企業がどう稼ぐのかを理解する。",
            "経済的な堀、経営陣の誠実さ、資本配分を長期価値の中核に置く。",
            "内在価値は精密な一点ではなく幅で捉え、安全域を確保する。",
            "機会が乏しいときは待ち、確信度が極めて高い機会には集中も認める。",
        ),
        "questions": (
            "市場が10年間閉鎖されても、この事業を保有し続けたいか？",
            "追加の留保利益を今後も高い収益率で再投資できるか？",
            "何が変われば、経済的な堀や経営陣への信頼が恒久的に損なわれるか？",
        ),
        "best_for": (
            "長期複利型の企業",
            "資本配分と経営陣の評価",
            "事業の質とバリュエーションの統合判断",
        ),
        "limitations": (
            "能力の輪の外にある企業や評価不能な企業を無理に低評価せず、「不明」とする。",
            "集中投資には高い確信度と十分な損失許容力が必要であり、誰にでもそのまま適用できるわけではない。",
        ),
    },
    "charlie-munger": {
        "name_ja": "チャーリー・マンガー",
        "school_ja": "学際的思考・逆算",
        "summary": (
            "逆算、複数分野の思考モデル、インセンティブ分析によって愚かな誤りを減らし、"
            "少数の高品質企業を優先するとともに、認知バイアスと破局的な失敗経路を重視する。"
        ),
        "principles": (
            "成功の道筋を考える前に、失敗する道筋を列挙する。",
            "経済学、心理学、数学、工学など複数のモデルで結論を交差検証する。",
            "インセンティブは経営陣、従業員、販売経路の行動を体系的に形づくる。",
            "巧妙な予測を追うより、明白な誤りを避ける方が一般に信頼できる。",
        ),
        "questions": (
            "どうすれば、この投資を台無しにできるか？",
            "関係者の実際の行動を動かしているインセンティブは何か？",
            "自分はアンカリング、確証バイアス、社会的証明の影響を同時に受けていないか？",
        ),
        "best_for": (
            "失敗経路と反証",
            "インセンティブ設計と企業文化",
            "認知バイアスの点検",
        ),
        "limitations": (
            "複数モデルの分析は後付けの物語になりやすいため、各モデルを検証可能な証拠に結びつける。",
            "公開資料にある警句を、本人による現在の企業への見解として扱わない。",
        ),
    },
    "duan-yongping": {
        "name_ja": "段永平（ドゥアン・ヨンピン）",
        "school_ja": "ビジネスモデル・企業文化",
        "summary": (
            "企業と将来キャッシュフローを買うという視点から、ビジネスモデル、差別化、"
            "企業文化、能力の輪を重視し、「やらないことリスト」でレバレッジ、投機、"
            "頻繁な売買を抑える。"
        ),
        "principles": (
            "良い事業には、差別化、顧客価値、持続可能なキャッシュフローがある。",
            "企業文化と「本分を守る」姿勢が、長期的な行動の境界を決める。",
            "理解できないものには投資せず、マクロ予測や短期株価予測で理解不足を補わない。",
            "新規投資は、現在得られる最良の機会との機会費用で測る。",
        ),
        "questions": (
            "なぜ良い事業なのかを、一文で説明できるか？",
            "短期利益より顧客価値を長期にわたって優先しているか？",
            "借入も株価の確認もできなくても、その企業を所有したいか？",
        ),
        "best_for": (
            "ビジネスモデルと差別化",
            "企業文化",
            "能力の輪と「やらないことリスト」",
        ),
        "limitations": (
            "ソーシャルメディア上の発言には時期と文脈があるため、原文へリンクし、発言そのものと要約を区別する。",
            "大まかな見積もりだけで、財務データの複数ソースによる検証を代替しない。",
        ),
    },
    "li-lu": {
        "name_ja": "李録（リー・ルー）",
        "school_ja": "クオリティ・バリュー",
        "summary": (
            "高品質企業を長期保有することを中心に据え、経済的な堀、成長余地、"
            "信頼できる経営陣、未知に誠実であること、資本の恒久的損失を避けることを重視する。"
        ),
        "principles": (
            "経済的な堀と成長余地を備えた高品質企業を長期保有する。",
            "信頼できる人物と誠実な文化を投資の前提条件とする。",
            "分かっていること、推論できること、分からないことを明確に分ける。",
            "機会が極めて少なく、確信度が非常に高い場合に限って集中を検討する。",
        ),
        "questions": (
            "20年後も、その企業は価値を生み続けている可能性が高いか？",
            "経営陣は、信頼に足る人間関係のネットワークの中にいるか？",
            "資本の恒久的損失をもたらす可能性が最も高い変数は何か？",
        ),
        "best_for": (
            "長期的な確実性",
            "信頼できる経営陣と企業文化",
            "恒久的損失のリスク",
        ),
        "limitations": (
            "文明の長期的傾向だけで、個別企業が価値を獲得できる証拠を代替しない。",
            "高度な集中は、証拠が十分で、それに見合うリスク許容力がある場合に限られる。",
        ),
    },
    "benjamin-graham": {
        "name_ja": "ベンジャミン・グレアム",
        "school_ja": "防御的バリュー",
        "summary": (
            "保守的に見積もった内在価値、財務上の安全性、安全域を中心に据え、"
            "再現可能な規律によって市場心理と予測誤差の影響を抑え、適切な分散で個別判断の失敗に備える。"
        ),
        "principles": (
            "価格が保守的な価値評価を大きく下回るときにのみ、安全域が生まれる。",
            "分析では、資産、収益力、財務の強さなど検証可能な事実を優先する。",
            "市場の変動は指示ではなく、価格提示の機会である。",
            "ルールには当時の時代背景と金利環境を明記し、過去の閾値を機械的に適用しない。",
        ),
        "questions": (
            "保守的な前提でも、価格は価値レンジの下限からどれだけ割安か？",
            "収益悪化や借り換え圧力に、貸借対照表は耐えられるか？",
            "期待した物語がすべて崩れた場合、残存価値と回収経路は何か？",
        ),
        "best_for": (
            "ディープバリューと資産価値からの乖離",
            "財務上の安全性",
            "候補群のルールベース・スクリーニング",
        ),
        "limitations": (
            "過去の固定倍率や債券利回りの閾値は、現在の環境に合わせて再調整する。",
            "単一のいわゆる「グレアム・ナンバー」を、哲学全体の代用にしない。",
        ),
    },
    "philip-fisher": {
        "name_ja": "フィリップ・フィッシャー",
        "school_ja": "クオリティ・グロース",
        "summary": (
            "長い成長余地、優れた研究開発・販売力、厚みのある経営組織、誠実な文化を備えた企業を探し、"
            "顧客、供給業者、競合などの公開情報で経営陣の説明を検証する。"
        ),
        "principles": (
            "成長の質は、市場余地、イノベーション効率、販売力、組織の厚みの組み合わせから生まれる。",
            "財務諸表だけでなく、複数種類の外部公開情報で会社の説明を検証する。",
            "悪い知らせに対する経営陣の率直さは、重要な品質シグナルである。",
            "高品質な成長企業は長期保有に向くが、買値を無視してよいわけではない。",
        ),
        "questions": (
            "成長余地は実際の顧客需要によるものか、それとも短期的な業界の追い風か？",
            "顧客、供給業者、元従業員、競合の公開情報は互いに整合しているか？",
            "創業者を超えて機能する、厚みのある経営組織があるか？",
        ),
        "best_for": (
            "高品質な成長企業",
            "研究開発・販売・組織能力",
            "外部情報による事実検証",
        ),
        "limitations": (
            "外部調査には公開された合法的な情報だけを使い、重要な未公開情報を誘導・収集しない。",
            "著作権で保護された原典のチェックリストは短く言い換え、まとまった部分を複製しない。",
        ),
    },
    "peter-lynch": {
        "name_ja": "ピーター・リンチ",
        "school_ja": "調査重視の成長株投資",
        "summary": (
            "身近な製品や業界から候補を見つけても、必ずファンダメンタルズ調査を行う。"
            "保有理由を平易な物語で説明し、成長株、景気循環株、再建株など企業の型に応じて"
            "本当の利益成長要因を追跡する。"
        ),
        "principles": (
            "日常の観察は手がかりにすぎず、買う根拠ではない。",
            "何を所有し、なぜ利益が伸びるのかを簡潔に説明できなければならない。",
            "企業の型が異なれば、調べる問いと売却条件も異なる。",
            "企業が不況を生き残れるかどうかは貸借対照表が決める。",
        ),
        "questions": (
            "保有理由と主要な利益成長要因を2分で説明できるか？",
            "成長、景気循環、安定、資産価値、再建のどの型に当たるか？",
            "現在の評価には、どれほど高い成長期待が織り込まれているか？",
        ),
        "best_for": (
            "消費関連企業と中小型の成長企業",
            "企業の型に応じた分岐分析",
            "簡潔な投資ストーリーと利益成長要因",
        ),
        "limitations": (
            "「知っているものを買う」を、製品が好きなら株を買うという意味に単純化しない。",
            "企業分類は問いを選ぶための経路であり、固定的な評価式ではない。",
        ),
    },
    "howard-marks": {
        "name_ja": "ハワード・マークス",
        "school_ja": "サイクル・リスク",
        "summary": (
            "良い資産と良い投資を区別し、価格に織り込まれた市場の共通期待、下方の結果分布、"
            "信用・心理サイクルに注目する。二次的思考によって、市場と異なり、かつより正しい判断を探す。"
        ),
        "principles": (
            "資産の質と投資魅力は同じではなく、価格と期待がリターンの余地を決める。",
            "リスクは単なる価格変動ではなく、結果の不確実性と恒久的損失で捉える。",
            "市場サイクルは、ファンダメンタルズ、信用環境、投資家心理が共に動かす。",
            "マクロ予測は頼りにくいが、現在のおおよその位置を見極め、複数シナリオに備えることはできる。",
        ),
        "questions": (
            "市場の共通見解は、すでに価格へ何を織り込んでいるか？",
            "自分の見方は市場とどこが異なり、なぜ自分の方が正しい可能性があるか？",
            "価値が価格に反映されるまで、資金面・心理面の双方で生き残れるか？",
        ),
        "best_for": (
            "価格と市場の共通期待",
            "信用・心理サイクル",
            "下方の結果と生存能力",
        ),
        "limitations": (
            "市場の温度は防御度を調整する材料であり、精密な売買タイミングの信号ではない。",
            "主観的なサイクル判断には、証拠、反証、確信度を添える。",
        ),
    },
    "john-bogle": {
        "name_ja": "ジョン・C・ボーグル",
        "school_ja": "低コスト・インデックス",
        "summary": (
            "低コストで広く分散された市場指数を通じて資本市場のリターンを得る。"
            "目標とリスク許容度に基づいて資産配分を決め、売買、税、感情が長期複利を損なう影響を抑える。"
        ),
        "principles": (
            "コスト、税、売買回転は、投資家が受け取るリターンを確実に削る。",
            "幅広い分散と簡潔な資産配分は、多くの投資家にとって強力な基準となる。",
            "直近の勝者を追うより、長期的な規律を守る方が通常は重要である。",
            "あらゆるアクティブ戦略を、低コスト指数の手取りリターンと比較する。",
        ),
        "questions": (
            "コスト、税、行動バイアスを差し引いても、アクティブ案に優位性はあるか？",
            "ポートフォリオは十分に分散され、利用者の期間と損失許容度に合っているか？",
            "複雑さは、証明可能な手取り便益を生んでいるか？",
        ),
        "best_for": (
            "アクティブ戦略を評価する基準ケース",
            "長期・低コストの資産配分",
            "コスト、税、行動によるリターン低下",
        ),
        "limitations": (
            "個別株の経済的な堀や経営陣を採点する枠組みではないため、適用範囲外では「該当なし」とする。",
            "指数投資でも、個人の目標とリスク許容度に合う資産配分が必要である。",
        ),
    },
    "ray-dalio": {
        "name_ja": "レイ・ダリオ／ブリッジウォーター",
        "school_ja": "マクロ・リスクバランス",
        "summary": (
            "単一の未来に賭けず、経済成長とインフレが予想を上回る・下回る各環境で資産の動きを検証し、"
            "名目金額ではなくリスク寄与度からポートフォリオが本当に分散されているかを捉える。"
        ),
        "principles": (
            "一点予測に依存せず、未来を複数の経済環境に分ける。",
            "名目金額が分散されていても、リスク源が分散されているとは限らない。",
            "相関と変動性はストレス時に変化するため、危機シナリオを別に検証する。",
            "原則を明文化すると振り返りやすくなるが、モデルのパラメータは常に疑う。",
        ),
        "questions": (
            "成長とインフレがそれぞれ予想を上回る、または下回るとき、ポートフォリオはどう動くか？",
            "どの単一リスク源が、ポートフォリオの損失を支配しているか？",
            "相関の急変、流動性の枯渇、デレバレッジが起きると何が生じるか？",
        ),
        "best_for": (
            "経済環境別のストレステスト",
            "リスク寄与度と相関",
            "ポートフォリオ単位の分散",
        ),
        "limitations": (
            "機関投資家向けのAll Weather実装を、個人向けの公式な複製として説明しない。",
            "一般利用者にはレバレッジを前提とせず、マクロ分析はストレステストに使い、短期予測には使わない。",
        ),
    },
    "joel-greenblatt": {
        "name_ja": "ジョエル・グリーンブラット",
        "school_ja": "システマティック・バリュー",
        "summary": (
            "企業価値に対する利益利回りや投下資本利益率などを用いて、相対的に割安な良い企業を探す。"
            "ルール、分散、十分に長い実行期間によって、個別判断の誤りと短期的な投資スタイルの不振を乗り越える。"
        ),
        "principles": (
            "企業の質と価格を別々に順位づけし、割安さだけで判断しない。",
            "ルールベースの候補群では、会計上の定義、除外業種、データ時点を明示する。",
            "分散保有と継続的な実行によって、個別の誤りと一時的な劣後に耐える。",
            "複雑なイベントでは、価値実現のカタリストと構造的リスクを個別に見極める。",
        ),
        "questions": (
            "高い投下資本利益率は、会計要因や景気循環の頂点ではなく、持続可能な事業から生じているか？",
            "企業価値、現金、リース、負債の定義は一貫しているか？",
            "どのカタリストによって、どの程度の期間で価値が実現しうるか？",
        ),
        "best_for": (
            "ルールベースのバリュー・スクリーニング",
            "企業の質と評価の二重順位づけ",
            "特殊状況とカタリスト",
        ),
        "limitations": (
            "公開資料だけでは公式スクリーナーを完全再現できないため、公式結果ではなく「Greenblatt型」と表示する。",
            "バックテストには当時点で利用可能だったデータを使い、上場廃止、コスト、税、流動性を織り込む。",
        ),
    },
}


_PROFILE_TEXT_FIELDS: Final[tuple[str, ...]] = (
    "summary",
    "principles",
    "questions",
    "best_for",
    "limitations",
)


def _require_object(value: Any, location: str) -> JsonObject:
    if not isinstance(value, Mapping):
        raise LocalizationError(f"{location} はobjectである必要があります")
    return deepcopy(dict(value))


def _require_string_id(value: Any, location: str) -> str:
    if not isinstance(value, str) or not value:
        raise LocalizationError(f"{location} は空でない文字列である必要があります")
    return value


def _require_list(value: Any, location: str) -> list[Any]:
    if not isinstance(value, list):
        raise LocalizationError(f"{location} は配列である必要があります")
    return value


def _label_ids(
    value: Any, labels: Mapping[str, str], location: str
) -> list[str]:
    identifiers = _require_list(value, location)
    localized: list[str] = []
    for index, raw_identifier in enumerate(identifiers):
        identifier = _require_string_id(raw_identifier, f"{location}[{index}]")
        try:
            localized.append(labels[identifier])
        except KeyError as exc:
            raise LocalizationError(
                f"{location}[{index}] に未翻訳の識別子があります: {identifier}"
            ) from exc
    return localized


def _investor_translation(investor_id: Any, location: str) -> InvestorTranslation:
    normalized_id = _require_string_id(investor_id, f"{location}.id")
    try:
        return INVESTOR_TRANSLATIONS_JA[normalized_id]
    except KeyError as exc:
        raise LocalizationError(
            f"{location}.id に対応する日本語訳がありません: {normalized_id}"
        ) from exc


def _localize_sources(value: Any, location: str) -> list[JsonObject]:
    sources = _require_list(value, location)
    localized_sources: list[JsonObject] = []
    for index, raw_source in enumerate(sources):
        source = _require_object(raw_source, f"{location}[{index}]")
        kind = _require_string_id(source.get("kind"), f"{location}[{index}].kind")
        try:
            source["kind_ja"] = SOURCE_KIND_LABELS_JA[kind]
        except KeyError as exc:
            raise LocalizationError(
                f"{location}[{index}].kind に対応する日本語ラベルがありません: {kind}"
            ) from exc
        localized_sources.append(source)
    return localized_sources


def _localize_investor_record(
    value: Any, location: str, *, require_full_profile: bool
) -> JsonObject:
    profile = _require_object(value, location)
    translation = _investor_translation(profile.get("id"), location)

    english_name = profile.get("name")
    if not isinstance(english_name, str) or not english_name:
        raise LocalizationError(f"{location}.name は空でない英語名である必要があります")

    school = _require_string_id(profile.get("school"), f"{location}.school")
    try:
        school_label = SCHOOL_LABELS_JA[school]
    except KeyError as exc:
        raise LocalizationError(
            f"{location}.school に対応する日本語ラベルがありません: {school}"
        ) from exc
    if school_label != translation["school_ja"]:
        raise LocalizationError(
            f"{location} の投資家訳と学派ラベルが一致しません"
        )

    if require_full_profile:
        missing = [field for field in _PROFILE_TEXT_FIELDS if field not in profile]
        if missing:
            raise LocalizationError(
                f"{location} に日本語化必須フィールドがありません: {', '.join(missing)}"
            )

    profile["name_ja"] = translation["name_ja"]
    profile["school_ja"] = school_label
    for field in _PROFILE_TEXT_FIELDS:
        if field not in profile:
            continue
        translated_value = translation[field]
        profile[field] = (
            translated_value
            if isinstance(translated_value, str)
            else list(translated_value)
        )

    if "scope" in profile:
        profile["scope_ja"] = _label_ids(
            profile["scope"], SCOPE_LABELS_JA, f"{location}.scope"
        )
    if "focus_tags" in profile:
        profile["focus_tags_ja"] = _label_ids(
            profile["focus_tags"], FOCUS_TAXONOMY_JA, f"{location}.focus_tags"
        )
    if "matched_focus" in profile:
        profile["matched_focus_ja"] = _label_ids(
            profile["matched_focus"],
            FOCUS_TAXONOMY_JA,
            f"{location}.matched_focus",
        )
    if "sources" in profile:
        profile["sources"] = _localize_sources(
            profile["sources"], f"{location}.sources"
        )
    return profile


def _require_exact_keys(
    value: Any, expected: Mapping[str, Any], location: str
) -> Mapping[str, Any]:
    if not isinstance(value, Mapping):
        raise LocalizationError(f"{location} はobjectである必要があります")
    actual_keys = set(value)
    expected_keys = set(expected)
    if actual_keys != expected_keys:
        missing = sorted(expected_keys - actual_keys)
        unknown = sorted(actual_keys - expected_keys)
        details: list[str] = []
        if missing:
            details.append("不足=" + ", ".join(missing))
        if unknown:
            details.append("未翻訳=" + ", ".join(unknown))
        raise LocalizationError(f"{location} の翻訳対応が不完全です ({'; '.join(details)})")
    return value


def localize_catalog(catalog: Mapping[str, Any]) -> JsonObject:
    """Return a deep-copied Japanese version of the ``view=meta`` catalog."""

    localized = _require_object(catalog, "catalog")
    taxonomy = _require_exact_keys(
        localized.get("focus_taxonomy"), FOCUS_TAXONOMY_JA, "catalog.focus_taxonomy"
    )
    localized["focus_taxonomy"] = {
        identifier: FOCUS_TAXONOMY_JA[identifier] for identifier in taxonomy
    }

    scenarios = _require_exact_keys(
        localized.get("scenarios"), SCENARIO_DESCRIPTIONS_JA, "catalog.scenarios"
    )
    localized_scenarios: JsonObject = {}
    for scenario_id, raw_scenario in scenarios.items():
        scenario = _require_object(raw_scenario, f"catalog.scenarios.{scenario_id}")
        scenario["description"] = SCENARIO_DESCRIPTIONS_JA[scenario_id]
        if "focus_tags" in scenario:
            scenario["focus_tags_ja"] = _label_ids(
                scenario["focus_tags"],
                FOCUS_TAXONOMY_JA,
                f"catalog.scenarios.{scenario_id}.focus_tags",
            )
        localized_scenarios[scenario_id] = scenario
    localized["scenarios"] = localized_scenarios

    investors = _require_list(localized.get("investors"), "catalog.investors")
    localized_investors = [
        _localize_investor_record(
            investor, f"catalog.investors[{index}]", require_full_profile=False
        )
        for index, investor in enumerate(investors)
    ]
    investor_ids = [investor["id"] for investor in localized_investors]
    if len(investor_ids) != len(set(investor_ids)):
        raise LocalizationError("catalog.investors に重複した投資家IDがあります")
    if set(investor_ids) != set(INVESTOR_TRANSLATIONS_JA):
        missing = sorted(set(INVESTOR_TRANSLATIONS_JA) - set(investor_ids))
        unknown = sorted(set(investor_ids) - set(INVESTOR_TRANSLATIONS_JA))
        details: list[str] = []
        if missing:
            details.append("不足=" + ", ".join(missing))
        if unknown:
            details.append("未翻訳=" + ", ".join(unknown))
        raise LocalizationError(
            "catalog.investors の日本語化対象が一致しません ("
            + "; ".join(details)
            + ")"
        )
    localized["investors"] = localized_investors
    localized["scope_labels"] = dict(SCOPE_LABELS_JA)
    localized["source_kind_labels"] = dict(SOURCE_KIND_LABELS_JA)
    localized["selection_mode_labels"] = dict(SELECTION_MODE_LABELS_JA)
    return localized


def localize_profile(profile: Mapping[str, Any]) -> JsonObject:
    """Return a deep-copied Japanese version of one complete investor profile."""

    return _localize_investor_record(
        profile, "profile", require_full_profile=True
    )


def localize_selection(selection: Mapping[str, Any]) -> JsonObject:
    """Return a deep-copied Japanese version of a selector result structure."""

    localized = _require_object(selection, "selection")
    scenario_id = _require_string_id(localized.get("scenario"), "selection.scenario")
    try:
        localized["scenario_description"] = SCENARIO_DESCRIPTIONS_JA[scenario_id]
    except KeyError as exc:
        raise LocalizationError(
            f"selection.scenario に対応する日本語訳がありません: {scenario_id}"
        ) from exc

    selection_mode = _require_string_id(
        localized.get("selection_mode"), "selection.selection_mode"
    )
    try:
        localized["selection_mode_ja"] = SELECTION_MODE_LABELS_JA[selection_mode]
    except KeyError as exc:
        raise LocalizationError(
            "selection.selection_mode に対応する日本語ラベルがありません: "
            + selection_mode
        ) from exc

    for field in (
        "focus_tags",
        "requested_focus_tags",
        "uncovered_focus_tags",
    ):
        localized[f"{field}_ja"] = _label_ids(
            localized.get(field), FOCUS_TAXONOMY_JA, f"selection.{field}"
        )

    selected_lenses = _require_list(
        localized.get("selected_lenses"), "selection.selected_lenses"
    )
    localized["selected_lenses"] = [
        _localize_investor_record(
            lens,
            f"selection.selected_lenses[{index}]",
            require_full_profile=True,
        )
        for index, lens in enumerate(selected_lenses)
    ]
    return localized


_EXPECTED_COUNTS: Final[tuple[int, int, int]] = (30, 7, 11)
if (
    len(FOCUS_TAXONOMY_JA),
    len(SCENARIO_DESCRIPTIONS_JA),
    len(INVESTOR_TRANSLATIONS_JA),
) != _EXPECTED_COUNTS:
    raise RuntimeError("日本語ローカライズ表の件数が契約と一致しません")
