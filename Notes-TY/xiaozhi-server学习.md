# xiaozhi-esp32-server 系统架构流程图

![image-20250724125037391](C:/Users/liuli/AppData/Roaming/Typora/typora-user-images/image-20250724125037391.png)



## 系统整体架构图

```mermaid
graph TB
    %% 用户和硬件层
    User[👤 用户]
    ESP32[🔊 ESP32设备<br/>智能硬件]
    Admin[👨‍💼 管理员]
    
    %% 核心服务层
    subgraph "核心AI引擎"
        XiaozhiServer["🧠 xiaozhi-server<br/>(Python - 端口8000)<br/>• WebSocket服务器<br/>• AI服务集成<br/>• 插件系统"]
    end
    
    %% 管理服务层
    subgraph "管理服务"
        ManagerAPI["⚙️ manager-api<br/>(Java Spring Boot - 端口8002)<br/>• RESTful API<br/>• 配置管理<br/>• 用户认证"]
        ManagerWeb["🌐 manager-web<br/>(Vue.js - 端口8001)<br/>• Web控制台<br/>• 系统配置界面"]
    end
    
    %% 数据存储层
    subgraph "数据存储"
        MySQL[(🗄️ MySQL<br/>持久化存储)]
        Redis[(⚡ Redis<br/>缓存存储)]
    end
    
    %% AI服务层
    subgraph "AI服务提供者"
        ASR[🎤 ASR<br/>语音识别]
        LLM[🤖 LLM<br/>大语言模型]
        TTS[🔊 TTS<br/>语音合成]
        VAD[📊 VAD<br/>语音活动检测]
        Memory[🧠 Memory<br/>对话记忆]
    end
    
    %% 插件系统
    subgraph "插件系统"
        Weather[🌤️ 天气查询]
        HomeAssistant[🏠 智能家居控制]
        IoTDevices[📱 IoT设备控制]
        CustomPlugins[🔧 自定义插件]
    end
    
    %% 用户交互流程
    User -.->|语音指令| ESP32
    ESP32 <-->|WebSocket<br/>音频流| XiaozhiServer
    ESP32 -.->|语音回复| User
    
    %% 管理流程
    Admin -->|浏览器访问| ManagerWeb
    ManagerWeb <-->|HTTP/JSON| ManagerAPI
    
    %% 配置同步
    XiaozhiServer <-->|HTTP请求<br/>获取配置| ManagerAPI
    
    %% 数据存储
    ManagerAPI <--> MySQL
    ManagerAPI <--> Redis
    
    %% AI服务集成
    XiaozhiServer --> ASR
    XiaozhiServer --> LLM
    XiaozhiServer --> TTS
    XiaozhiServer --> VAD
    XiaozhiServer --> Memory
    
    %% 插件调用
    XiaozhiServer --> Weather
    XiaozhiServer --> HomeAssistant
    XiaozhiServer --> IoTDevices
    XiaozhiServer --> CustomPlugins
    
    %% 样式定义
    classDef userClass fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef coreClass fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef manageClass fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef dataClass fill:#fff3e0,stroke:#e65100,stroke-width:2px
    classDef aiClass fill:#fce4ec,stroke:#880e4f,stroke-width:2px
    classDef pluginClass fill:#f1f8e9,stroke:#33691e,stroke-width:2px
    
    class User,ESP32,Admin userClass
    class XiaozhiServer coreClass
    class ManagerAPI,ManagerWeb manageClass
    class MySQL,Redis dataClass
    class ASR,LLM,TTS,VAD,Memory aiClass
    class Weather,HomeAssistant,IoTDevices,CustomPlugins pluginClass
```

## 语音交互详细流程图

```mermaid
sequenceDiagram
    participant User as 👤 用户
    participant ESP32 as 🔊 ESP32设备
    participant WS as 🌐 WebSocket服务器
    participant VAD as 📊 VAD检测
    participant ASR as 🎤 ASR识别
    participant LLM as 🤖 LLM处理
    participant Plugins as 🔧 插件系统
    participant TTS as 🔊 TTS合成
    participant Memory as 🧠 记忆模块
    
    User->>ESP32: 语音指令
    ESP32->>WS: WebSocket连接建立
    ESP32->>WS: 音频数据流(二进制)
    
    WS->>VAD: 音频数据
    VAD->>WS: 语音活动检测结果
    
    alt 检测到有效语音
        WS->>ASR: 语音片段
        ASR->>WS: 识别文本
        
        WS->>Memory: 获取对话历史
        Memory->>WS: 上下文信息
        
        WS->>LLM: 文本+上下文+可用函数
        LLM->>WS: 理解结果+回复文本
        
        alt 需要调用插件
            WS->>Plugins: 函数调用请求
            Plugins->>WS: 执行结果
            WS->>LLM: 插件执行结果
            LLM->>WS: 最终回复文本
        end
        
        WS->>Memory: 更新对话历史
        WS->>TTS: 回复文本
        TTS->>WS: 合成语音
        
        WS->>ESP32: 语音数据流(二进制)
        ESP32->>User: 播放语音回复
    end
```

## 管理配置流程图

```mermaid
sequenceDiagram
    participant Admin as 👨‍💼 管理员
    participant Web as 🌐 manager-web
    participant API as ⚙️ manager-api
    participant MySQL as 🗄️ MySQL
    participant Redis as ⚡ Redis
    participant XZServer as 🧠 xiaozhi-server
    
    Admin->>Web: 浏览器访问控制台
    Web->>API: 用户登录请求
    API->>MySQL: 验证用户信息
    MySQL->>API: 用户认证结果
    API->>Web: 登录成功+Token
    
    Admin->>Web: 修改AI服务配置
    Web->>API: HTTP请求(配置更新)
    API->>MySQL: 保存配置到数据库
    API->>Redis: 更新缓存
    API->>Web: 配置保存成功
    
    XZServer->>API: 请求最新配置
    API->>Redis: 查询缓存
    alt 缓存命中
        Redis->>API: 返回配置数据
    else 缓存未命中
        API->>MySQL: 查询数据库
        MySQL->>API: 配置数据
        API->>Redis: 更新缓存
    end
    API->>XZServer: 返回配置数据
    XZServer->>XZServer: 重新初始化AI模块
```

## 系统部署架构图

```mermaid
graph TB
    subgraph "Docker容器部署"
        subgraph "容器1: xiaozhi-server"
            XS[xiaozhi-server:8000]
        end
        
        subgraph "容器2: manager-api"
            MA[manager-api:8002]
        end
        
        subgraph "容器3: manager-web"
            MW[manager-web:8001]
        end
        
        subgraph "容器4: 数据库"
            DB[(MySQL:3306)]
            CACHE[(Redis:6379)]
        end
    end
    
    subgraph "外部服务"
        CloudAI[☁️ 云端AI服务<br/>OpenAI/Azure/等]
        LocalAI[💻 本地AI模型<br/>FunASR/本地LLM]
    end
    
    subgraph "硬件设备"
        ESP32Devices[📱 ESP32设备群]
    end
    
    subgraph "用户界面"
        Browser[🌐 浏览器管理界面]
    end
    
    %% 连接关系
    ESP32Devices <-->|WebSocket| XS
    Browser -->|HTTP| MW
    MW <-->|API调用| MA
    XS <-->|配置获取| MA
    MA <--> DB
    MA <--> CACHE
    XS --> CloudAI
    XS --> LocalAI
    
    %% 端口映射
    XS -.->|映射| Port8000[Host:8000]
    MA -.->|映射| Port8002[Host:8002]
    MW -.->|映射| Port8001[Host:8001]
    
    classDef containerClass fill:#e3f2fd,stroke:#1565c0,stroke-width:2px
    classDef serviceClass fill:#f1f8e9,stroke:#558b2f,stroke-width:2px
    classDef deviceClass fill:#fce4ec,stroke:#c2185b,stroke-width:2px
    
    class XS,MA,MW,DB,CACHE containerClass
    class CloudAI,LocalAI serviceClass
    class ESP32Devices,Browser deviceClass
```

## 技术栈总览

```mermaid
mindmap
  root((xiaozhi-esp32-server))
    核心AI引擎
      Python 3
      Asyncio异步编程
      WebSocket通信
      Provider模式
      插件系统
    管理后端
      Java 21
      Spring Boot 3
      MyBatis-Plus
      Apache Shiro
      MySQL数据库
      Redis缓存
    Web前端
      Vue.js 2
      Element UI
      Vuex状态管理
      Vue Router
      PWA特性
    AI服务集成
      ASR语音识别
      LLM大语言模型
      TTS语音合成
      VAD语音检测
      Memory对话记忆
    部署方案
      Docker容器化
      源码部署
      环境配置
      动态配置
```

## 数据流向图

```mermaid
flowchart LR
    subgraph "输入层"
        A[用户语音] --> B[ESP32设备]
        C[管理员操作] --> D[Web界面]
    end
    
    subgraph "处理层"
        B --> E[WebSocket服务]
        D --> F[RESTful API]
        E --> G[AI处理流水线]
        F --> H[配置管理]
    end
    
    subgraph "AI处理流水线"
        G --> I[VAD检测]
        I --> J[ASR识别]
        J --> K[LLM理解]
        K --> L[插件执行]
        L --> M[TTS合成]
    end
    
    subgraph "存储层"
        H --> N[(MySQL)]
        H --> O[(Redis)]
    end
    
    subgraph "输出层"
        M --> P[语音回复]
        N --> Q[配置同步]
        O --> R[缓存加速]
    end
    
    P --> B
    Q --> E
    R --> F
```

---

> 本流程图基于 xiaozhi-esp32-server 项目的技术文档创建，展示了系统的整体架构、核心组件交互、数据流向和部署方案。该系统是一个功能完整的ESP32智能语音助手后端解决方案。

