// 分类 —— 对应亮哥游戏库左侧栏
const CATEGORIES = [
  "亮哥推荐", "苹果游戏(IOS)", "萌灵社", "主讯", "狼来了",
  "久游", "北京柚享", "无极", "翱翔", "灵动",
  "聚合汇", "猫咪", "小鱼", "测快手专用", "栀子乐园"
];

// 游戏数据 —— 改这里即可增删游戏
// cat 必须是上面 CATEGORIES 之一；link 为真实下载/跳转地址（示例用 #）
const GAMES = [
  {id:1, title:"方块消除大师", icon:"🧩", cat:"亮哥推荐", tags:["三消","轻松"], desc:"经典三消玩法，数百关卡挑战眼力与策略。", size:"12MB", date:"2026-08-29", plays:9821, link:"#"},
  {id:2, title:"合成大西瓜", icon:"🍉", cat:"亮哥推荐", tags:["合成","上头"], desc:"合成相同水果，直到种出巨型西瓜！", size:"8MB", date:"2026-08-29", plays:32105, link:"#"},
  {id:3, title:"节奏音游", icon:"🎵", cat:"亮哥推荐", tags:["音乐","节奏"], desc:"跟着节拍点击音符，享受音乐快感。", size:"35MB", date:"2026-08-28", plays:11200, link:"#"},
  {id:4, title:"开心钓鱼", icon:"🎣", cat:"亮哥推荐", tags:["放置","治愈"], desc:"宁静湖畔抛竿垂钓，填满图鉴。", size:"20MB", date:"2026-08-24", plays:5430, link:"#"},

  {id:5, title:"水果忍者", icon:"🥷", cat:"苹果游戏(IOS)", tags:["切水果","爽快"], desc:"挥刀切水果，小心别切到炸弹！", size:"13MB", date:"2026-08-27", plays:16700, link:"#"},
  {id:6, title:"糖果传奇", icon:"🍬", cat:"苹果游戏(IOS)", tags:["三消","可爱"], desc:"交换糖果组成三个或更多，解锁新世界。", size:"25MB", date:"2026-08-23", plays:22100, link:"#"},
  {id:7, title:"跳跃忍者", icon:"🥷", cat:"苹果游戏(IOS)", tags:["跑酷","反应"], desc:"化身忍者不断向前跳跃，躲避陷阱。", size:"15MB", date:"2026-08-26", plays:12088, link:"#"},

  {id:8, title:"萌灵小镇", icon:"🌸", cat:"萌灵社", tags:["养成","治愈"], desc:"收集可爱灵兽，打造你的梦幻小镇。", size:"42MB", date:"2026-08-28", plays:8800, link:"#"},
  {id:9, title:"梦幻花园", icon:"🌷", cat:"萌灵社", tags:["经营","放松"], desc:"布置花园、照料花朵，治愈你的心情。", size:"30MB", date:"2026-08-22", plays:6400, link:"#"},

  {id:10, title:"主讯快讯", icon:"📡", cat:"主讯", tags:["资讯","工具"], desc:"聚合游戏资讯与攻略，一手掌握。", size:"6MB", date:"2026-08-29", plays:3200, link:"#"},
  {id:11, title:"速算达人", icon:"🔢", cat:"主讯", tags:["益智","烧脑"], desc:"限时口算挑战，锻炼你的反应力。", size:"5MB", date:"2026-08-21", plays:5100, link:"#"},

  {id:12, title:"狼人推理", icon:"🐺", cat:"狼来了", tags:["桌游","社交"], desc:"语言推理社交游戏，找出隐藏的狼人。", size:"28MB", date:"2026-08-25", plays:7600, link:"#"},
  {id:13, title:"荒野求生", icon:"🏕️", cat:"狼来了", tags:["生存","冒险"], desc:"孤身闯入荒野，采集资源活下去。", size:"46MB", date:"2026-08-20", plays:9200, link:"#"},

  {id:14, title:"久游棋牌", icon:"🀄", cat:"久游", tags:["棋牌","休闲"], desc:"经典棋牌合集，随时随地来一局。", size:"22MB", date:"2026-08-19", plays:11300, link:"#"},
  {id:15, title:"泡泡龙", icon:"🫧", cat:"久游", tags:["弹射","经典"], desc:"发射泡泡匹配同色消除，经典爽快。", size:"11MB", date:"2026-08-18", plays:6500, link:"#"},

  {id:16, title:"柚享农场", icon:"🍊", cat:"北京柚享", tags:["经营","治愈"], desc:"种植柚子与其他作物，打造繁荣农场。", size:"33MB", date:"2026-08-24", plays:4700, link:"#"},

  {id:17, title:"无极剑道", icon:"⚔️", cat:"无极", tags:["动作","热血"], desc:"修炼剑术连招，挑战强敌成为剑豪。", size:"44MB", date:"2026-08-17", plays:8100, link:"#"},

  {id:18, title:"翱翔飞行", icon:"✈️", cat:"翱翔", tags:["飞行","冒险"], desc:"驾驶飞机穿越云层，探索广阔天空。", size:"40MB", date:"2026-08-16", plays:5900, link:"#"},

  {id:19, title:"灵动拼图", icon:"🖼️", cat:"灵动", tags:["拼图","放松"], desc:"把碎片拼成完整图画，海量精美图库。", size:"16MB", date:"2026-08-15", plays:3800, link:"#"},

  {id:20, title:"聚合资讯", icon:"📰", cat:"聚合汇", tags:["资讯","聚合"], desc:"游戏资讯一站式聚合阅读。", size:"7MB", date:"2026-08-23", plays:2900, link:"#"},

  {id:21, title:"猫咪公寓", icon:"🐱", cat:"猫咪", tags:["养成","治愈"], desc:"收养可爱猫咪，布置温馨公寓。", size:"31MB", date:"2026-08-22", plays:10200, link:"#"},

  {id:22, title:"小鱼池塘", icon:"🐟", cat:"小鱼", tags:["放置","治愈"], desc:"养殖各色小鱼，装点你的水族箱。", size:"18MB", date:"2026-08-20", plays:4500, link:"#"},

  {id:23, title:"快手测试", icon:"🎬", cat:"测快手专用", tags:["工具","测试"], desc:"快手内容创作辅助小工具。", size:"9MB", date:"2026-08-28", plays:1600, link:"#"},

  {id:24, title:"栀子物语", icon:"🌼", cat:"栀子乐园", tags:["经营","治愈"], desc:"打理栀子花园，收获芬芳与故事。", size:"29MB", date:"2026-08-21", plays:5300, link:"#"},
];
