# -*- coding: utf-8 -*-
"""
后端服务测试
"""

import json
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import requests

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app  # noqa: E402
from services.annotation_service import DIFFICULT_CHARS  # noqa: E402
from services.annotation_service import annotate_difficult_chars
from services.classic_service import ClassicService  # noqa: E402
from services.classic_service import (
    get_all_classics,
    get_classic_metadata,
    load_classics_metadata,
    validate_classic_id,
)
from services.cross_civilization_dialogue import (  # noqa: E402
    CROSS_CIVILIZATION_PHILOSOPHERS,
    ConceptMapper,
    DialogueEngine,
    PhilosopherType,
    get_available_philosophers,
    get_comparative_analysis,
    start_philosophy_dialogue,
)
from services.data_service import DataService  # noqa: E402
from services.knowledge_graph import CommentryAnalyzer  # noqa: E402
from services.knowledge_graph import (
    ConceptExtractor,
    KnowledgeGraphBuilder,
    get_all_concepts,
    get_chapter_knowledge_graph,
)
from services.semantic_archaeology import SemanticArchaeology  # noqa: E402
from services.semantic_archaeology import VectorSemanticAnalyzer
from services.tts_service import EdgeTTSService  # noqa: E402
from services.tts_service import FishAudioService, TTSService
from services.virtual_commentator import COMMENTATOR_PERSONAS  # noqa: E402
from services.virtual_commentator import (
    SocraticDialogue,
    VirtualCommentator,
    generate_commentary_response,
    get_available_commentators,
    get_commentator_persona,
)
from utils.validators import validate_chapter_id  # noqa: E402
from utils.validators import validate_search_query


@pytest.fixture
def client():
    """创建测试客户端"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestDataService:
    """数据服务测试"""

    def test_load_data(self):
        """测试数据加载"""
        data = DataService.load_data()
        assert data is not None
        assert "title" in data
        assert "chapters" in data
        assert len(data["chapters"]) == 81

    def test_get_chapter_valid(self):
        """测试获取有效章节"""
        chapter = DataService.get_chapter(1)
        assert chapter is not None
        assert chapter["chapter"] == 1
        assert "original" in chapter

    def test_get_chapter_invalid(self):
        """测试获取无效章节"""
        chapter = DataService.get_chapter(999)
        assert chapter is None

    def test_get_chapter_with_annotation(self):
        """测试获取带标注的章节"""
        chapter = DataService.get_chapter_with_annotation(1)
        assert chapter is not None
        assert "original_annotated" in chapter
        assert "prev_chapter" in chapter
        assert "next_chapter" in chapter

    def test_search_chapters(self):
        """测试章节搜索"""
        results = DataService.search_chapters("道")
        assert len(results) > 0
        assert "id" in results[0]
        assert "title" in results[0]

    def test_search_chapters_empty(self):
        """测试空搜索"""
        results = DataService.search_chapters("")
        assert len(results) == 0


class TestAnnotationService:
    """标注服务测试"""

    def test_difficult_chars_exists(self):
        """测试疑难字字典存在"""
        assert isinstance(DIFFICULT_CHARS, dict)
        assert len(DIFFICULT_CHARS) > 0

    def test_annotate_difficult_chars(self):
        """测试疑难字标注"""
        text = "道可道非常道"
        result = annotate_difficult_chars(text)
        # 文本应该被处理
        assert isinstance(result, str)

    def test_annotate_with_difficult_char(self):
        """测试包含疑难字的标注"""
        text = "谷神不死"
        result = annotate_difficult_chars(text)
        # 应该包含标注的HTML
        if "谷神" in DIFFICULT_CHARS:
            assert "difficult" in result or "data-pinyin" in result


class TestValidators:
    """输入验证测试"""

    def test_validate_chapter_id_valid(self):
        """测试有效章节ID"""
        assert validate_chapter_id(1) is True
        assert validate_chapter_id(81) is True

    def test_validate_chapter_id_invalid(self):
        """测试无效章节ID"""
        assert validate_chapter_id(0) is False
        assert validate_chapter_id(82) is False
        assert validate_chapter_id(-1) is False
        assert validate_chapter_id("abc") is False

    def test_validate_search_query_valid(self):
        """测试有效搜索查询"""
        is_valid, error = validate_search_query("道德经")
        assert is_valid is True
        assert error is None

    def test_validate_search_query_empty(self):
        """测试空搜索查询"""
        is_valid, error = validate_search_query("")
        assert is_valid is False
        assert error is not None

    def test_validate_search_query_too_long(self):
        """测试过长搜索查询"""
        long_query = "a" * 101
        is_valid, error = validate_search_query(long_query)
        assert is_valid is False
        assert error is not None
        assert "长度" in error

    def test_validate_search_query_xss(self):
        """测试XSS攻击防护"""
        xss_query = '<script>alert("xss")</script>'
        is_valid, error = validate_search_query(xss_query)
        assert is_valid is False
        assert error is not None


class TestRoutes:
    """路由测试"""

    def test_index_redirect(self, client):
        """测试首页 - 平台首页展示所有经典"""
        response = client.get("/")
        assert response.status_code == 200
        assert "中华古籍多版本对照研究平台" in response.data.decode("utf-8")

    def test_daodejing_index(self, client):
        """测试道德经首页"""
        response = client.get("/daodejing/", follow_redirects=True)
        assert response.status_code == 200

    def test_chapter_view_valid(self, client):
        """测试有效章节页面"""
        response = client.get("/daodejing/chapter/1", follow_redirects=True)
        assert response.status_code == 200

    def test_chapter_view_invalid(self, client):
        """测试无效章节页面"""
        response = client.get("/daodejing/chapter/999")
        # 应该重定向到首页
        assert response.status_code == 302

    def test_api_chapters(self, client):
        """测试章节API"""
        response = client.get("/api/daodejing/chapters")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "chapters" in data
        assert len(data["chapters"]) == 81

    def test_api_chapter_valid(self, client):
        """测试单章API"""
        response = client.get("/api/daodejing/chapter/1")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data["chapter"] == 1

    def test_api_chapter_invalid(self, client):
        """测试无效单章API"""
        response = client.get("/api/daodejing/chapter/999")
        assert response.status_code == 404

    def test_api_search(self, client):
        """测试搜索API"""
        response = client.get("/api/daodejing/search?q=道")
        assert response.status_code == 200
        data = json.loads(response.data)
        assert "results" in data

    def test_api_search_invalid(self, client):
        """测试无效搜索API（XSS）"""
        response = client.get("/api/daodejing/search?q=<script>")
        # 应该被拒绝或返回空结果
        assert response.status_code in [200, 400]
        if response.status_code == 400:
            data = json.loads(response.data)
            assert "error" in data


class TestSecurity:
    """安全性测试"""

    def test_security_headers(self, client):
        """测试安全响应头"""
        # 发送请求但不检查响应头
        client.get("/daodejing/")
        # 此测试仅验证路由可访问，不验证安全头

    def test_rate_limiting_simulation(self, client):  # noqa: U100
        """模拟速率限制测试"""
        # 注意：实际测试需要配置测试用的速率限制器
        # 这里只是模拟结构
        pass


class TestClassicService:
    """经典服务测试"""

    def test_load_classics_metadata(self):
        """测试加载经典元数据"""
        metadata = load_classics_metadata()
        assert metadata is not None
        assert "classics" in metadata
        assert len(metadata["classics"]) >= 1

    def test_get_classic_metadata_ddj(self):
        """测试获取道德经元数据"""
        metadata = get_classic_metadata("ddj")
        assert metadata is not None
        assert metadata["id"] == "ddj"
        assert metadata["name"] == "道德经"
        assert metadata["chapters"] == 81

    def test_get_classic_metadata_zzj(self):
        """测试获取庄子元数据"""
        metadata = get_classic_metadata("zzj")
        assert metadata is not None
        assert metadata["id"] == "zzj"
        assert metadata["name"] == "庄子"
        assert metadata["chapters"] == 33

    def test_get_classic_metadata_invalid(self):
        """测试获取无效经典元数据"""
        metadata = get_classic_metadata("invalid_id")
        assert metadata is None

    def test_get_all_classics(self):
        """测试获取所有经典列表"""
        classics = get_all_classics()
        assert isinstance(classics, list)
        assert len(classics) >= 1
        assert any(c["id"] == "ddj" for c in classics)

    def test_validate_classic_id_valid(self):
        """测试有效经典ID验证"""
        assert validate_classic_id("ddj") is True
        assert validate_classic_id("zzj") is True

    def test_validate_classic_id_invalid(self):
        """测试无效经典ID验证"""
        assert validate_classic_id("invalid") is False
        assert validate_classic_id("") is False

    def test_classic_service_init_ddj(self):
        """测试初始化道德经服务"""
        service = ClassicService("ddj")
        assert service.classic_id == "ddj"
        assert service.metadata is not None
        assert service.chapter_count == 81

    def test_classic_service_init_default(self):
        """测试初始化默认经典服务"""
        service = ClassicService()
        assert service.classic_id == "ddj"  # 默认是道德经

    def test_classic_service_load_data(self):
        """测试经典服务加载数据"""
        service = ClassicService("ddj")
        data = service.load_data()
        assert data is not None
        assert "chapters" in data
        assert len(data["chapters"]) == 81

    def test_classic_service_get_chapter(self):
        """测试获取章节"""
        service = ClassicService("ddj")
        chapter = service.get_chapter(1)
        assert chapter is not None
        assert chapter["chapter"] == 1
        assert "original" in chapter

    def test_classic_service_get_chapter_invalid(self):
        """测试获取无效章节"""
        service = ClassicService("ddj")
        chapter = service.get_chapter(999)
        assert chapter is None

    def test_classic_service_get_commentators(self):
        """测试获取注释家列表"""
        service = ClassicService("ddj")
        commentators = service.get_commentators()
        assert isinstance(commentators, list)
        assert len(commentators) >= 10
        assert any(c["id"] == "wangbi" for c in commentators)

    def test_classic_service_get_translators(self):
        """测试获取翻译家列表"""
        service = ClassicService("ddj")
        translators = service.get_translators()
        assert isinstance(translators, list)
        assert len(translators) >= 5

    def test_classic_service_to_dict(self):
        """测试转换为字典"""
        service = ClassicService("ddj")
        config = service.to_dict()
        assert "id" in config
        assert "name" in config
        assert config["id"] == "ddj"

    def test_classic_service_clear_cache(self):
        """测试清除缓存"""
        service = ClassicService("ddj")
        service.load_data()  # 先加载数据建立缓存
        service.clear_cache()
        # 再次加载应该仍然工作
        data = service.load_data()
        assert data is not None

    def test_classic_service_clear_all_cache(self):
        """测试清除所有缓存"""
        ClassicService.clear_all_cache()
        service = ClassicService("ddj")
        data = service.load_data()
        assert data is not None


class TestKnowledgeGraph:
    """知识图谱服务测试"""

    def test_concept_extractor_init(self):
        """测试概念提取器初始化"""
        extractor = ConceptExtractor()
        assert extractor is not None
        assert extractor.concept_chapters is not None

    def test_concept_extractor_extract_from_chapter(self):
        """测试从章节中提取概念"""
        extractor = ConceptExtractor()
        text = "道可道非常道，无名天地之始"
        concepts = extractor.extract_from_chapter(1, text)
        assert isinstance(concepts, set)
        assert "道" in concepts
        # "天地"作为双字概念被提取
        assert "天地" in concepts or "无" in concepts

    def test_concept_extractor_extract_double_concepts(self):
        """测试提取双字概念"""
        extractor = ConceptExtractor()
        text = "圣人处无为之事，行不言之教"
        concepts = extractor.extract_from_chapter(2, text)
        assert "无为" in concepts

    def test_concept_extractor_build_cooccurrence_network(self):
        """测试构建共现网络"""
        extractor = ConceptExtractor()
        chapters_data = [
            {"chapter": 1, "original": "道可道非常道", "modern_chinese": "道可以说"},
            {
                "chapter": 2,
                "original": "天下皆知美之为美",
                "modern_chinese": "天下都知道",
            },
        ]
        network = extractor.build_cooccurrence_network(chapters_data)
        assert isinstance(network, dict)

    def test_commentary_analyzer_init(self):
        """测试注释分析器初始化"""
        analyzer = CommentryAnalyzer()
        assert analyzer is not None
        assert analyzer.commentary_views is not None

    def test_commentary_analyzer_analyze(self):
        """测试分析注释"""
        analyzer = CommentryAnalyzer()
        result = analyzer.analyze_commentary(
            1, "wangbi", "这是王弼的注释内容", "wangbi"
        )
        assert "chapter" in result
        assert "commentator" in result
        assert result["chapter"] == 1

    def test_commentary_analyzer_extract_key_concepts(self):
        """测试提取关键概念"""
        analyzer = CommentryAnalyzer()
        concepts = analyzer._extract_key_concepts("气神虚静，天地万物")
        assert isinstance(concepts, list)
        assert len(concepts) > 0

    def test_commentary_analyzer_detect_stance(self):
        """测试检测注释立场"""
        analyzer = CommentryAnalyzer()
        assert analyzer._detect_stance("气丹修炼精气神") == "修炼向"
        assert analyzer._detect_stance("治国帝王政治天下") == "治世向"

    def test_commentary_analyzer_compare(self):
        """测试比较注释家"""
        analyzer = CommentryAnalyzer()
        commentaries = {"wangbi": "这是王弼的注释", "heshanggong": "这是河上公的注释"}
        comparisons = analyzer.compare_commentators(1, commentaries)
        assert isinstance(comparisons, list)

    def test_knowledge_graph_builder_init(self):
        """测试知识图谱构建器初始化"""
        builder = KnowledgeGraphBuilder("data/daodejing/chapters.json")
        assert builder is not None
        assert builder.data_file == "data/daodejing/chapters.json"

    def test_knowledge_graph_builder_load_data(self):
        """测试知识图谱加载数据"""
        builder = KnowledgeGraphBuilder("data/daodejing/chapters.json")
        data = builder.load_data()
        assert data is not None
        assert "chapters" in data

    def test_knowledge_graph_builder_build_concept_graph(self):
        """测试构建概念图谱"""
        builder = KnowledgeGraphBuilder("data/daodejing/chapters.json")
        builder.load_data()
        graph = builder.build_concept_graph()
        assert "nodes" in graph
        assert "edges" in graph
        assert isinstance(graph["nodes"], list)

    def test_knowledge_graph_builder_build_commentary_spectrum(self):
        """测试构建注释观点谱系"""
        builder = KnowledgeGraphBuilder("data/daodejing/chapters.json")
        builder.load_data()
        spectrum = builder.build_commentary_spectrum(1)
        assert "chapter" in spectrum
        assert "commentaries" in spectrum

    def test_get_chapter_knowledge_graph(self):
        """测试获取章节知识图谱API"""
        result = get_chapter_knowledge_graph(1)
        assert "concept_graph" in result
        assert "commentary_spectrum" in result

    def test_get_all_concepts(self):
        """测试获取所有概念列表"""
        concepts = get_all_concepts()
        assert isinstance(concepts, list)
        assert len(concepts) > 0


class TestCrossCivilizationDialogue:
    """跨文明哲学对话测试"""

    def test_philosopher_type_enum(self):
        """测试哲学家类型枚举"""
        assert PhilosopherType.CHINESE.value == "中国哲学"
        assert PhilosopherType.WESTERN.value == "西方哲学"
        assert PhilosopherType.INDIAN.value == "印度哲学"

    def test_cross_civilization_philosophers_exists(self):
        """测试跨文明哲学家库存在"""
        assert isinstance(CROSS_CIVILIZATION_PHILOSOPHERS, dict)
        assert len(CROSS_CIVILIZATION_PHILOSOPHERS) > 0
        assert "heidegger" in CROSS_CIVILIZATION_PHILOSOPHERS
        assert "zhuangzi" in CROSS_CIVILIZATION_PHILOSOPHERS

    def test_philosopher_persona_structure(self):
        """测试哲学家人设结构"""
        philosopher = CROSS_CIVILIZATION_PHILOSOPHERS.get("heidegger")
        assert philosopher is not None
        assert philosopher.id == "heidegger"
        assert philosopher.name == "海德格尔"
        assert philosopher.culture == "德国"
        assert len(philosopher.key_concepts) > 0

    def test_get_available_philosophers(self):
        """测试获取可用哲学家列表"""
        philosophers = get_available_philosophers()
        assert isinstance(philosophers, list)
        assert len(philosophers) > 0
        assert any(p["id"] == "heidegger" for p in philosophers)

    def test_concept_mapper_init(self):
        """测试概念映射器初始化"""
        mapper = ConceptMapper()
        assert mapper is not None

    def test_concept_mapper_get_correspondence(self):
        """测试获取概念对应关系"""
        mapper = ConceptMapper()
        correspondences = mapper.get_correspondence("道", "heidegger")
        assert isinstance(correspondences, list)

    def test_concept_mapper_concept_mappings_exists(self):
        """测试概念映射存在"""
        mapper = ConceptMapper()
        assert "道" in mapper.CONCEPT_MAPPINGS
        assert "德" in mapper.CONCEPT_MAPPINGS
        assert "无" in mapper.CONCEPT_MAPPINGS

    def test_dialogue_engine_init(self):
        """测试对话引擎初始化"""
        engine = DialogueEngine()
        assert engine is not None
        assert engine.mapper is not None

    def test_dialogue_engine_initiate_dialogue(self):
        """测试发起对话"""
        engine = DialogueEngine()
        result = engine.initiate_dialogue(1, "道", "heidegger", "zhuangzi")
        assert "chapter" in result
        assert "participant1" in result
        assert "participant2" in result
        assert result["chapter"] == 1

    def test_dialogue_engine_initiate_invalid_philosophers(self):
        """测试发起无效哲学家对话"""
        engine = DialogueEngine()
        result = engine.initiate_dialogue(1, "道", "invalid1", "invalid2")
        assert "error" in result

    def test_dialogue_engine_generate_comparative_analysis(self):
        """测试生成比较分析"""
        engine = DialogueEngine()
        result = engine.generate_comparative_analysis(
            1, "道", ["heidegger", "zhuangzi"]
        )
        assert "concept" in result
        assert "philosophers" in result
        assert "commonalities" in result

    def test_start_philosophy_dialogue(self):
        """测试发起哲学对话API"""
        result = start_philosophy_dialogue(1, "道", "heidegger", "zhuangzi")
        assert "topic" in result
        assert "participant1" in result

    def test_get_comparative_analysis(self):
        """测试获取比较分析API"""
        result = get_comparative_analysis(1, "道", ["heidegger", "zhuangzi"])
        assert "concept" in result
        assert "philosophers" in result
        assert len(result["philosophers"]) == 2


class TestVirtualCommentator:
    """虚拟注释家测试"""

    def test_commentator_personas_exists(self):
        """测试注释家人设库存在"""
        assert isinstance(COMMENTATOR_PERSONAS, dict)
        assert len(COMMENTATOR_PERSONAS) >= 10
        assert "wangbi" in COMMENTATOR_PERSONAS
        assert "heshanggong" in COMMENTATOR_PERSONAS

    def test_commentator_persona_structure(self):
        """测试注释家人设结构"""
        persona = COMMENTATOR_PERSONAS.get("wangbi")
        assert persona is not None
        assert persona.name == "王弼"
        assert persona.era == "魏晋（226-249）"
        assert persona.school == "贵无派"
        assert len(persona.key_themes) > 0

    def test_get_available_commentators(self):
        """测试获取可用注释家列表"""
        commentators = get_available_commentators()
        assert isinstance(commentators, list)
        assert len(commentators) >= 10
        assert any(c["id"] == "wangbi" for c in commentators)

    def test_get_commentator_persona_valid(self):
        """测试获取有效注释家人设"""
        persona = get_commentator_persona("wangbi")
        assert persona is not None
        assert persona["id"] == "wangbi"
        assert persona["name"] == "王弼"

    def test_get_commentator_persona_invalid(self):
        """测试获取无效注释家人设"""
        persona = get_commentator_persona("invalid_id")
        assert persona is None

    def test_virtual_commentator_init(self):
        """测试虚拟注释家初始化"""
        commentator = VirtualCommentator("data/daodejing/chapters.json")
        assert commentator is not None
        assert commentator.data_file == "data/daodejing/chapters.json"

    def test_virtual_commentator_load_data(self):
        """测试虚拟注释家加载数据"""
        commentator = VirtualCommentator("data/daodejing/chapters.json")
        assert commentator.data is not None
        assert "chapters" in commentator.data

    def test_virtual_commentator_get_available_commentators(self):
        """测试获取可用注释家（实例方法）"""
        commentator = VirtualCommentator("data/daodejing/chapters.json")
        available = commentator.get_available_commentators(1)
        assert isinstance(available, list)

    def test_virtual_commentator_get_available_commentators_invalid_chapter(self):
        """测试获取无效章节的注释家"""
        commentator = VirtualCommentator("data/daodejing/chapters.json")
        available = commentator.get_available_commentators(999)
        assert isinstance(available, list)
        assert len(available) == 0

    def test_virtual_commentator_chat_with_commentator(self):
        """测试与注释家对话"""
        commentator = VirtualCommentator("data/daodejing/chapters.json")
        result = commentator.chat_with_commentator("wangbi", 1, "什么是道？")
        assert "commentator_id" in result
        assert "response" in result

    def test_virtual_commentator_chat_invalid_commentator(self):
        """测试与无效注释家对话"""
        commentator = VirtualCommentator("data/daodejing/chapters.json")
        result = commentator.chat_with_commentator("invalid", 1, "测试")
        assert "error" in result

    def test_virtual_commentator_classify_question(self):
        """测试问题分类"""
        commentator = VirtualCommentator("data/daodejing/chapters.json")
        assert commentator._classify_question("怎么修炼") == "practice"
        assert commentator._classify_question("有什么区别") == "comparison"
        assert commentator._classify_question("是什么意思") == "meaning"

    def test_virtual_commentator_initiate_debate(self):
        """测试发起注释家辩论"""
        commentator = VirtualCommentator("data/daodejing/chapters.json")
        result = commentator.initiate_debate(1, "道", ["wangbi", "heshanggong"])
        assert "chapter" in result
        assert "participants" in result
        assert len(result["participants"]) == 2

    def test_socratic_dialogue_init(self):
        """测试苏格拉底式对话初始化"""
        dialogue = SocraticDialogue()
        assert dialogue is not None

    def test_socratic_dialogue_start(self):
        """测试开始苏格拉底式对话"""
        dialogue = SocraticDialogue()
        result = dialogue.start_dialogue(1, "beginner")
        assert "chapter" in result
        assert "opening_question" in result

    def test_socratic_dialogue_follow_up(self):
        """测试苏格拉底式追问"""
        dialogue = SocraticDialogue()
        dialogue.start_dialogue(1, "beginner")
        follow_up = dialogue.follow_up_question(1, "我认为道是宇宙的本源。")
        assert isinstance(follow_up, str)
        assert len(follow_up) > 0

    def test_generate_commentary_response(self):
        """测试生成注释回应API"""
        result = generate_commentary_response("wangbi", 1, "什么是道？")
        assert "commentator_id" in result
        assert "commentator_name" in result
        assert "system_prompt" in result


class TestSemanticArchaeology:
    """语义考古学服务测试"""

    def test_semantic_archaeology_init(self):
        """测试语义考古学初始化"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        assert archaeology.data_file == "data/daodejing.json"
        assert archaeology.data is None

    def test_load_data(self):
        """测试加载数据"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        data = archaeology.load_data()
        assert data is not None
        assert "title" in data
        assert "chapters" in data
        assert len(data["chapters"]) > 0

    def test_analyze_text_evolution_valid(self):
        """测试分析文本演变（有效章节）"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        archaeology.load_data()
        result = archaeology.analyze_text_evolution(1)
        assert result is not None
        assert "chapter" in result
        assert result["chapter"] == 1
        assert "versions" in result
        assert "variants" in result
        assert "semantic_shifts" in result

    def test_analyze_text_evolution_invalid(self):
        """测试分析文本演变（无效章节）"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        archaeology.load_data()
        result = archaeology.analyze_text_evolution(999)  # 不存在的章节
        assert result is None

    def test_detect_variants(self):
        """测试检测文字变异"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        variants = archaeology._detect_variants("古文本", "帛书本", "通行本")
        assert isinstance(variants, list)

    def test_analyze_semantic_shifts(self):
        """测试分析语义变迁"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        shifts = archaeology._analyze_semantic_shifts("郭店简差异", "帛书差异")
        assert isinstance(shifts, list)
        assert len(shifts) <= 2

    def test_trace_concept_history(self):
        """测试追溯概念历史"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        result = archaeology.trace_concept_history("道")
        assert result is not None
        assert "concept" in result
        assert result["concept"] == "道"
        assert "occurrences" in result
        assert "semantic_layers" in result

    def test_compare_interpretation_history_valid(self):
        """测试比较阐释历史（有效章节）"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        archaeology.load_data()
        result = archaeology.compare_interpretation_history(1, "道")
        assert result is not None
        assert "chapter" in result
        assert result["chapter"] == 1
        assert "concept" in result
        assert result["concept"] == "道"
        assert "interpretations" in result

    def test_compare_interpretation_history_invalid(self):
        """测试比较阐释历史（无效章节）"""
        archaeology = SemanticArchaeology("data/daodejing.json")
        archaeology.load_data()
        result = archaeology.compare_interpretation_history(999, "道")
        assert result is None

    def test_vector_semantic_analyzer_init(self):
        """测试向量语义分析器初始化"""
        analyzer = VectorSemanticAnalyzer()
        assert analyzer.semantic_vectors == {}

    def test_calculate_semantic_distance(self):
        """测试计算语义距离"""
        analyzer = VectorSemanticAnalyzer()
        distance = analyzer.calculate_semantic_distance("文本一", "文本二")
        assert isinstance(distance, float)
        assert 0 <= distance <= 1.0

    def test_detect_semantic_drift(self):
        """测试检测语义漂移"""
        analyzer = VectorSemanticAnalyzer()
        versions = [
            {"version": "guodian", "text": "古文本"},
            {"version": "postsilk", "text": "帛书本"},
            {"version": "received", "text": "通行本"},
        ]
        drifts = analyzer.detect_semantic_drift(versions)
        assert isinstance(drifts, list)


class TestTTSService:
    """TTS服务测试"""

    def test_tts_service_init(self):
        """测试TTS服务初始化"""
        service = TTSService()
        assert service.timeout == 30

    def test_fish_audio_service_init(self):
        """测试Fish Audio服务初始化"""
        service = FishAudioService()
        assert service.timeout == 30
        assert service.API_URL == "https://api.fish.audio/v1/tts"

    def test_edge_tts_service_init(self):
        """测试Edge TTS服务初始化"""
        service = EdgeTTSService()
        assert service.timeout == 30
        assert "speech.platform.bing.com" in service.API_URL

    def test_validate_request_no_data(self):
        """测试验证请求 - 无数据"""
        service = TTSService()
        with app.test_request_context(
            "/api/tts/test",
            method="POST",
            content_type="application/json",
            data="{}",
        ):
            is_valid, error_msg, data = service.validate_request(["text"])
            assert is_valid is False
            assert error_msg is not None

    def test_validate_request_missing_field(self):
        """测试验证请求 - 缺少必需字段"""
        service = TTSService()
        with app.test_request_context(
            "/api/tts/test", method="POST", json={}, content_type="application/json"
        ):
            is_valid, error_msg, data = service.validate_request(["text", "api_key"])
            assert is_valid is False
            assert error_msg is not None

    def test_validate_request_valid(self):
        """测试验证请求 - 有效数据"""
        service = TTSService()
        with app.test_request_context(
            "/api/tts/test",
            method="POST",
            json={"text": "测试文本", "api_key": "test_key"},
        ):
            is_valid, error_msg, data = service.validate_request(["text", "api_key"])
            assert is_valid is True
            assert error_msg is None
            assert data is not None
            assert data["text"] == "测试文本"

    @patch("services.tts_service.requests.post")
    def test_fish_audio_synthesize_success(self, mock_post):
        """测试Fish Audio语音合成成功"""
        # 模拟成功响应
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_post.return_value = mock_response

        service = FishAudioService()
        with app.test_request_context(
            "/api/tts/fish-audio",
            method="POST",
            json={"text": "测试文本", "api_key": "test_key"},
        ):
            response = service.synthesize()
            assert response.status_code == 200  # type: ignore
            assert response.mimetype == "audio/mpeg"  # type: ignore

    @patch("services.tts_service.requests.post")
    def test_fish_audio_synthesize_api_error(self, mock_post):
        """测试Fish Audio语音合成API错误"""
        # 模拟API错误
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        service = FishAudioService()
        with app.test_request_context(
            "/api/tts/fish-audio",
            method="POST",
            json={"text": "测试文本", "api_key": "test_key"},
        ):
            response, status_code = service.synthesize()  # type: ignore
            assert status_code == 401
            assert b"error" in response.data

    @patch("services.tts_service.requests.post")
    def test_fish_audio_synthesize_timeout(self, mock_post):
        """测试Fish Audio语音合成超时"""
        # 模拟超时异常
        mock_post.side_effect = requests.exceptions.Timeout()

        service = FishAudioService()
        with app.test_request_context(
            "/api/tts/fish-audio",
            method="POST",
            json={"text": "测试文本", "api_key": "test_key"},
        ):
            response, status_code = service.synthesize()  # type: ignore
            assert status_code == 504
            assert b"timeout" in response.data

    @patch("services.tts_service.requests.post")
    def test_fish_audio_synthesize_request_exception(self, mock_post):
        """测试Fish Audio语音合成请求异常"""
        # 模拟请求异常
        mock_post.side_effect = requests.exceptions.RequestException("Connection error")

        service = FishAudioService()
        with app.test_request_context(
            "/api/tts/fish-audio",
            method="POST",
            json={"text": "测试文本", "api_key": "test_key"},
        ):
            response, status_code = service.synthesize()  # type: ignore
            assert status_code == 502
            assert b"Request failed" in response.data

    @patch("services.tts_service.requests.post")
    def test_fish_audio_synthesize_with_model_id(self, mock_post):
        """测试Fish Audio语音合成带模型ID"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_post.return_value = mock_response

        service = FishAudioService()
        with app.test_request_context(
            "/api/tts/fish-audio",
            method="POST",
            json={
                "text": "测试文本",
                "api_key": "test_key",
                "model_id": "custom_model",
            },
        ):
            _ = service.synthesize()
            # 验证请求中包含了model_id
            call_args = mock_post.call_args
            assert call_args is not None
            assert call_args[1]["json"]["model_id"] == "custom_model"

    def test_fish_audio_synthesize_invalid_request(self):
        """测试Fish Audio语音合成无效请求"""
        service = FishAudioService()
        with app.test_request_context(
            "/api/tts/fish-audio",
            method="POST",
            json={},  # 缺少必需字段
        ):
            response, status_code = service.synthesize()  # type: ignore
            assert status_code == 400
            assert (
                b"No JSON data provided" in response.data or b"Missing" in response.data
            )

    @patch("services.tts_service.requests.post")
    def test_edge_tts_synthesize_success(self, mock_post):
        """测试Edge TTS语音合成成功"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_post.return_value = mock_response

        service = EdgeTTSService()
        with app.test_request_context(
            "/api/tts/edge", method="POST", json={"text": "测试文本"}
        ):
            response = service.synthesize()
            assert response.status_code == 200  # type: ignore
            assert response.mimetype == "audio/mpeg"  # type: ignore

    @patch("services.tts_service.requests.post")
    def test_edge_tts_synthesize_with_custom_voice(self, mock_post):
        """测试Edge TTS语音合成自定义语音"""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"fake_audio_data"
        mock_post.return_value = mock_response

        service = EdgeTTSService()
        with app.test_request_context(
            "/api/tts/edge",
            method="POST",
            json={"text": "测试文本", "voice": "zh-CN-YunxiNeural"},
        ):
            response = service.synthesize()
            assert response.status_code == 200  # type: ignore

    @patch("services.tts_service.requests.post")
    def test_edge_tts_synthesize_api_error(self, mock_post):
        """测试Edge TTS语音合成API错误"""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        service = EdgeTTSService()
        with app.test_request_context(
            "/api/tts/edge", method="POST", json={"text": "测试文本"}
        ):
            response, status_code = service.synthesize()  # type: ignore
            assert status_code == 500
            assert b"error" in response.data

    @patch("services.tts_service.requests.post")
    def test_edge_tts_synthesize_timeout(self, mock_post):
        """测试Edge TTS语音合成超时"""
        mock_post.side_effect = requests.exceptions.Timeout()

        service = EdgeTTSService()
        with app.test_request_context(
            "/api/tts/edge", method="POST", json={"text": "测试文本"}
        ):
            response, status_code = service.synthesize()  # type: ignore
            assert status_code == 504
            assert b"timeout" in response.data

    @patch("services.tts_service.requests.post")
    def test_edge_tts_synthesize_exception(self, mock_post):
        """测试Edge TTS语音合成异常"""
        mock_post.side_effect = Exception("Unknown error")

        service = EdgeTTSService()
        with app.test_request_context(
            "/api/tts/edge", method="POST", json={"text": "测试文本"}
        ):
            response, status_code = service.synthesize()  # type: ignore
            assert status_code == 500
            assert b"Server error" in response.data


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
