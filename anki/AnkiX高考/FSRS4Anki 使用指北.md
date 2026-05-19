# FSRS4Anki 使用指北

> [原文链接](https://zhuanlan.zhihu.com/p/636564830)

阅读须知：该教程只适用于 Anki 2.1.62-2.1.66。新版本的教程在此：[Anki 新算法 FSRS 配置指南](https://zhuanlan.zhihu.com/p/664758200)。

## 0 介绍

FSRS4Anki，即 Free Spaced Repetition Scheduler for Anki，一款能在 Anki 上运行的自由、开源的间隔重复调度算法。相较于 Anki 内置的、有着长达 30 年历史的 SM-2 算法，FSRS 更新、更准、更强。

FSRS4Anki 主要分为三个部分：Scheduler（调度器）、Optimizer（优化器）和 Helper（助手插件）。

Scheduler 可以根据当前卡片的记忆状态、复习间隔和复习打分来预测记忆状态的变化，并给出合适的复习间隔。
Optimizer 可以根据学习者上传的历史复习记录，生成拟合学习者记忆情况的模型权重。
Helper 以 FSRS 记忆状态为核心，允许学习者更加灵活地复习。

以下是 FSRS4Anki 的使用教程。

## 1 快速上手

### 1.1 开启 Anki 的 V3 排程算法

勾选设置>复习>启用 V3 排程算法 

![](https://picx.zhimg.com/v2-dfe932d39e85a2d38632c8399f2f5f33_1440w.jpg)
### 1.2 粘贴 FSRS 算法代码

![](https://pica.zhimg.com/v2-42fb9d2cbf89ea427b4504df273477a0_1440w.jpg)
在牌组选项中，找到高级设置一栏，在自定义排程中粘贴以下代码：

// FSRS4Anki v4.3.0 Scheduler Qt6
set_version();
// The latest version will be released on https://github.com/open-spaced-repetition/fsrs4anki/releases/latest

// Configuration Start

const deckParams = [
  {
    // Default parameters of FSRS4Anki for global
    &#34;deckName&#34;: &#34;global config for FSRS4Anki&#34;,
    &#34;w&#34;: [0.4, 0.6, 2.4, 5.8, 4.93, 0.94, 0.86, 0.01, 1.49, 0.14, 0.94, 2.18, 0.05, 0.34, 1.26, 0.29, 2.61],
    // The above parameters can be optimized via FSRS4Anki optimizer.
    // For details about the parameters, please see: https://github.com/open-spaced-repetition/fsrs4anki/wiki/The-Algorithm
    // User&#39;s custom parameters for global
    &#34;requestRetention&#34;: 0.9, // recommended setting: 0.8 ~ 0.9
    &#34;maximumInterval&#34;: 36500,
    // FSRS only modifies the long-term scheduling. So (re)learning steps in deck options work as usual.
    // I recommend setting steps shorter than 1 day.
  },
  {
    // Example 1: User&#39;s custom parameters for this deck and its sub-decks.
    &#34;deckName&#34;: &#34;MainDeck1&#34;,
    &#34;w&#34;: [0.6, 0.9, 2.9, 6.8, 4.72, 1.02, 1, 0.04, 1.49, 0.17, 1.02, 2.15, 0.07, 0.35, 1.17, 0.32, 2.53],
    &#34;requestRetention&#34;: 0.9,
    &#34;maximumInterval&#34;: 36500,
  },
  {
    // Example 2: User&#39;s custom parameters for this deck and its sub-decks.
    // Don&#39;t omit any keys.
    &#34;deckName&#34;: &#34;MainDeck2::SubDeck::SubSubDeck&#34;,
    &#34;w&#34;: [0.6, 0.9, 2.9, 6.8, 4.72, 1.02, 1, 0.04, 1.49, 0.17, 1.02, 2.15, 0.07, 0.35, 1.17, 0.32, 2.53],
    &#34;requestRetention&#34;: 0.9,
    &#34;maximumInterval&#34;: 36500,
  }
];

// To turn off FSRS in specific decks, fill them into the skip_decks list below.
// Please don&#39;t remove it even if you don&#39;t need it.
const skip_decks = [&#34;MainDeck3&#34;, &#34;MainDeck4::SubDeck&#34;];

// &#34;Fuzz&#34; is a small random delay applied to new intervals to prevent cards from
// sticking together and always coming up for review on the same day
const enable_fuzz = true;

// FSRS supports displaying memory states of cards.
// Enable it for debugging if you encounter something wrong.
const display_memory_state = false;

// Configuration End

debugger;

// display if FSRS is enabled
if (display_memory_state) {
  const prev = document.getElementById(&#39;FSRS_status&#39;)
  if (prev) { prev.remove(); }
  var fsrs_status = document.createElement(&#39;span&#39;);
  fsrs_status.innerHTML = &#34;FSRS enabled&#34;;
  fsrs_status.id = &#34;FSRS_status&#34;;
  fsrs_status.style.cssText = &#34;font-size:12px;opacity:0.5;font-family:monospace;text-align:left;line-height:1em;&#34;;
  document.body.appendChild(fsrs_status);
  document.getElementById(&#34;qa&#34;).style.cssText += &#34;min-height:50vh;&#34;;
}
let params = {};
// get the name of the card&#39;s deck
if (deck_name = get_deckname()) {
  if (display_memory_state) {
    fsrs_status.innerHTML += &#34;Deck name: &#34; + deck_name;
  }
  for (const i of skip_decks) {
    if (deck_name.startsWith(i)) {
      fsrs_status.innerHTML = fsrs_status.innerHTML.replace(&#34;FSRS enabled&#34;, &#34;FSRS disabled&#34;);
      return;
    }
  }
  // Arrange the deckParams of sub-decks in front of their parent decks.
  deckParams.sort(function(a, b) {
    return -a.deckName.localeCompare(b.deckName);
  });
  for (let i = 0; i Deck name not found&#34;;
  }
}
if (Object.keys(params).length === 0) {
  params = deckParams.find(deck => deck.deckName === &#34;global config for FSRS4Anki&#34;);
}
var w = params[&#34;w&#34;];
var requestRetention = params[&#34;requestRetention&#34;];
var maximumInterval = params[&#34;maximumInterval&#34;];
// auto-calculate intervalModifier
const intervalModifier = 9 * (1 / requestRetention - 1);
// global fuzz factor for all ratings.
const fuzz_factor = set_fuzz_factor();
const ratings = {
  &#34;again&#34;: 1,
  &#34;hard&#34;: 2,
  &#34;good&#34;: 3,
  &#34;easy&#34;: 4
};
// For new cards
if (is_new()) {
  init_states();
  const good_interval = next_interval(customData.good.s);
  const easy_interval = Math.max(next_interval(customData.easy.s), good_interval + 1);
  if (states.good.normal?.review) {
    states.good.normal.review.scheduledDays = good_interval;
  }
  if (states.easy.normal?.review) {
    states.easy.normal.review.scheduledDays = easy_interval;
  }
  // For learning/relearning cards
} else if (is_learning()) {
  // Init states if the card didn&#39;t contain customData
  if (is_empty()) {
    init_states();
  }
  const good_interval = next_interval(customData.good.s);
  const easy_interval = Math.max(next_interval(customData.easy.s), good_interval + 1);
  if (states.good.normal?.review) {
    states.good.normal.review.scheduledDays = good_interval;
  }
  if (states.easy.normal?.review) {
    states.easy.normal.review.scheduledDays = easy_interval;
  }
  // For review cards
} else if (is_review()) {
  // Convert the interval and factor to stability and difficulty if the card didn&#39;t contain customData
  if (is_empty()) {
    convert_states();
  }
  const interval = states.current.normal?.review.elapsedDays ? states.current.normal.review.elapsedDays : states.current.filtered.rescheduling.originalState.review.elapsedDays;
  const last_d = customData.again.d;
  const last_s = customData.again.s;
  const retrievability = Math.pow(1 + interval / (9 * last_s), -1)
  if (display_memory_state) {
    fsrs_status.innerHTML += &#34;D: &#34; + last_d + &#34;S: &#34; + last_s + &#34;R: &#34; + (retrievability * 100).toFixed(2) + &#34;%&#34;;
  }
  customData.again.d = next_difficulty(last_d, &#34;again&#34;);
  customData.again.s = next_forget_stability(customData.again.d, last_s, retrievability);
  customData.hard.d = next_difficulty(last_d, &#34;hard&#34;);
  customData.hard.s = next_recall_stability(customData.hard.d, last_s, retrievability, &#34;hard&#34;);
  customData.good.d = next_difficulty(last_d, &#34;good&#34;);
  customData.good.s = next_recall_stability(customData.good.d, last_s, retrievability, &#34;good&#34;);
  customData.easy.d = next_difficulty(last_d, &#34;easy&#34;);
  customData.easy.s = next_recall_stability(customData.easy.d, last_s, retrievability, &#34;easy&#34;);
  let hard_interval = next_interval(customData.hard.s);
  let good_interval = next_interval(customData.good.s);
  let easy_interval = next_interval(customData.easy.s);
  hard_interval = Math.min(hard_interval, good_interval)
  good_interval = Math.max(good_interval, hard_interval + 1);
  easy_interval = Math.max(easy_interval, good_interval + 1);
  if (states.hard.normal?.review) {
    states.hard.normal.review.scheduledDays = hard_interval;
  }
  if (states.good.normal?.review) {
    states.good.normal.review.scheduledDays = good_interval;
  }
  if (states.easy.normal?.review) {
    states.easy.normal.review.scheduledDays = easy_interval;
  }
}
function constrain_difficulty(difficulty) {
  return Math.min(Math.max(+difficulty.toFixed(2), 1), 10);
}
function apply_fuzz(ivl) {
  if (!enable_fuzz || ivl  scheduledDays) {
      min_ivl = Math.max(min_ivl, scheduledDays + 1);
    }
  }
  return Math.floor(fuzz_factor * (max_ivl - min_ivl + 1) + min_ivl);
}
function next_interval(stability) {
  const new_interval = apply_fuzz(stability * intervalModifier);
  return Math.min(Math.max(Math.round(new_interval), 1), maximumInterval);
}
function next_difficulty(d, rating) {
  let next_d = d - w[6] * (ratings[rating] - 3);
  return constrain_difficulty(mean_reversion(w[4], next_d));
}
function mean_reversion(init, current) {
  return w[7] * init + (1 - w[7]) * current;
}
function next_recall_stability(d, s, r, rating) {
  let hardPenalty = rating === &#34;hard&#34; ? w[15] : 1;
  let easyBonus = rating === &#34;easy&#34; ? w[16] : 1;
  return +(s * (1 + Math.exp(w[8]) *
    (11 - d) *
    Math.pow(s, -w[9]) *
    (Math.exp((1 - r) * w[10]) - 1) *
    hardPenalty *
    easyBonus)).toFixed(2);
}
function next_forget_stability(d, s, r) {
  return +Math.min(w[11] * 
    Math.pow(d, -w[12]) * 
    (Math.pow(s + 1, w[13]) - 1) * 
    Math.exp((1 - r) * w[14]), s).toFixed(2);
}
function init_states() {
  customData.again.d = init_difficulty(&#34;again&#34;);
  customData.again.s = init_stability(&#34;again&#34;);
  customData.hard.d = init_difficulty(&#34;hard&#34;);
  customData.hard.s = init_stability(&#34;hard&#34;);
  customData.good.d = init_difficulty(&#34;good&#34;);
  customData.good.s = init_stability(&#34;good&#34;);
  customData.easy.d = init_difficulty(&#34;easy&#34;);
  customData.easy.s = init_stability(&#34;easy&#34;);
}
function init_difficulty(rating) {
  return +constrain_difficulty(w[4] - w[5] * (ratings[rating] - 3)).toFixed(2);
}
function init_stability(rating) {
  return +Math.max(w[ratings[rating] - 1], 0.1).toFixed(2);
}
function convert_states() {
  const scheduledDays = states.current.normal ? states.current.normal.review.scheduledDays : states.current.filtered.rescheduling.originalState.review.scheduledDays;
  const easeFactor = states.current.normal ? states.current.normal.review.easeFactor : states.current.filtered.rescheduling.originalState.review.easeFactor;
  const old_s = +Math.max(scheduledDays, 0.1).toFixed(2);
  const old_d = constrain_difficulty(11 - (easeFactor - 1) / (Math.exp(w[8]) * Math.pow(old_s, -w[9]) * (Math.exp(0.1 * w[10]) - 1)));
  customData.again.d = old_d;
  customData.again.s = old_s;
  customData.hard.d = old_d;
  customData.hard.s = old_s;
  customData.good.d = old_d;
  customData.good.s = old_s;
  customData.easy.d = old_d;
  customData.easy.s = old_s;
}
function is_new() {
  if (states.current.normal?.new !== undefined) {
    if (states.current.normal?.new !== null) {
      return true;
    }
  }
  if (states.current.filtered?.rescheduling?.originalState !== undefined) {
    if (Object.hasOwn(states.current.filtered?.rescheduling?.originalState, &#39;new&#39;)) {
      return true;
    }
  }
  return false;
}
function is_learning() {
  if (states.current.normal?.learning !== undefined) {
    if (states.current.normal?.learning !== null) {
      return true;
    }
  }
  if (states.current.filtered?.rescheduling?.originalState !== undefined) {
    if (Object.hasOwn(states.current.filtered?.rescheduling?.originalState, &#39;learning&#39;)) {
      return true;
    }
  }
  if (states.current.normal?.relearning !== undefined) {
    if (states.current.normal?.relearning !== null) {
      return true;
    }
  }
  if (states.current.filtered?.rescheduling?.originalState !== undefined) {
    if (Object.hasOwn(states.current.filtered?.rescheduling?.originalState, &#39;relearning&#39;)) {
      return true;
    }
  }
  return false;
}
function is_review() {
  if (states.current.normal?.review !== undefined) {
    if (states.current.normal?.review !== null) {
      return true;
    }
  }
  if (states.current.filtered?.rescheduling?.originalState !== undefined) {
    if (Object.hasOwn(states.current.filtered?.rescheduling?.originalState, &#39;review&#39;)) {
      return true;
    }
  }
  return false;
}
function is_empty() {
  return !customData.again.d | !customData.again.s | !customData.hard.d | !customData.hard.s | !customData.good.d | !customData.good.s | !customData.easy.d | !customData.easy.s;
}
function set_version() {
  const version = &#34;v4.3.0&#34;;
  customData.again.v = version;
  customData.hard.v = version;
  customData.good.v = version;
  customData.easy.v = version;
}
function get_deckname() {
  if (typeof ctx !== &#39;undefined&#39; && ctx.deckName) {
    return ctx.deckName;
  } else if (document.getElementById(&#34;deck&#34;) !== null && document.getElementById(&#34;deck&#34;).getAttribute(&#34;deck_name&#34;)) {
    return document.getElementById(&#34;deck&#34;).getAttribute(&#34;deck_name&#34;);
  } else {
    return null;
  }
}
function get_seed() {
  if (!customData.again.seed | !customData.hard.seed | !customData.good.seed | !customData.easy.seed) {
    if (typeof ctx !== &#39;undefined&#39; && ctx.seed) {
      return ctx.seed;
    } else {
      return document.getElementById(&#34;qa&#34;).innerText;
    }
  } else {
    return customData.good.seed;
  }
}
function set_fuzz_factor() {
  // Note: Originally copied from seedrandom.js package (https://github.com/davidbau/seedrandom)
  !function(f,a,c){var s,l=256,p=&#34;random&#34;,d=c.pow(l,6),g=c.pow(2,52),y=2*g,h=l-1;function n(n,t,r){function e(){for(var n=u.g(6),t=d,r=0;n>>=1;return(n+r)/t}var o=[],i=j(function n(t,r){var e,o=[],i=typeof t;if(r&&&#34;object&#34;==i)for(e in t)try{o.push(n(t[e],r-1))}catch(n){}return o.length?o:&#34;string&#34;==i?t:t+&#34;\0&#34;}((t=1==t?{entropy:!0}:t||{}).entropy?[n,S(a)]:null==n?function(){try{var n;return s&&(n=s.randomBytes)?n=n(l):(n=new Uint8Array(l),(f.crypto||f.msCrypto).getRandomValues(n)),S(n)}catch(n){var t=f.navigator,r=t&&t.plugins;return[+new Date,f,r,f.screen,S(a)]}}():n,3),o),u=new m(o);return e.int32=function(){return 0|u.g(4)},e.quick=function(){return u.g(4)/4294967296},e.double=e,j(S(u.S),a),(t.pass||r||function(n,t,r,e){return e&&(e.S&&v(e,u),n.state=function(){return v(u,{})}),r?(c[p]=n,t):n})(e,i,&#34;global&#34;in t?t.global:this==c,t.state)}function m(n){var t,r=n.length,u=this,e=0,o=u.i=u.j=0,i=u.S=[];for(r||(n=[r++]);e> 最新稳定版本的代码请见：[Releases · open-spaced-repetition/fsrs4anki (github.com)](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki/releases/latest)
理论上你已经开始使用 FSRS4Anki 算法了。如果你不确定，可以将代码中的

const display_memory_state = false;
改为

const display_memory_state = true;
然后随便打开一个牌组复习，你将看到：

![](https://pic4.zhimg.com/v2-0b84dfc2066520eac05cc1809e6f4b75_1440w.jpg)
这表示你的 FSRS 已经正常运行了。然后你可以再把代码改回去，就不会显示这个信息了。

## 2 进阶使用

### 2.1 生成个性化参数

[fsrs4anki/fsrs4anki_optimizer.ipynb at main · open-spaced-repetition/fsrs4anki](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki/blob/main/fsrs4anki_optimizer.ipynb)打开 optimizer 的 notebook，点击 Open in Colab，即可在 Google Colab 上运行优化器，不需要自己配置代码运行环境，还可以白嫖 Google 的机器（需要注册 Google 账号）：

![](https://pic2.zhimg.com/v2-51b327eb51a7664947981b1e2f7b625d_1440w.jpg)
在 Colab 上打开后，切到文件夹标签页，然后等 Optimizer 连上 Google 的机器，就可以右键上传你的牌组文件/集合文件了。请在导出这些文件时，勾选「包含学习进度信息」以及「支持较旧的Anki版本」。

![](https://pic1.zhimg.com/v2-c0d71b46b1429929c8176c4bed80b66a_1440w.jpg)

![](https://pica.zhimg.com/v2-f6beee55d26bc4447ae7ea7a67a071b6_1440w.jpg)
传完后，把 notebook 里的 filename 改成你上传的文件名称。

![](https://pic3.zhimg.com/v2-d606ba6bf7ae0c44c13b48d7c28ec048_1440w.jpg)
然后点击「全部运行」

![](https://pic4.zhimg.com/v2-c28ee6a502c71cf49f46291cdd2e5ac1_1440w.jpg)
然后到 2.3 节等到代码跑完，复制输出的个性化参数。

![](https://pica.zhimg.com/v2-401ac9df90c09eb859221f90f79e18c8_1440w.jpg)
替换前面你复制的 FSRS 代码中的参数。

![](https://pic1.zhimg.com/v2-59158f2b7a9c23c0a7ae1561bb214ca6_1440w.jpg)
⚠️注意：替换这个参数的时候，请不要把结尾的逗号给删掉了。

### 2.2 牌组参数设置

你也可以为不同牌组生成不同的参数，并在代码中分别配置。在默认配置中，deckParams 已经包含了三组参数。

global config for FSRS4Anki 这组是全局参数。

ALL::Learning::English::Reading 这组是应用于 ALL::Learning::English::Reading 这个牌组及其子牌组的参数。

 同理，第三组就是应用于 ALL::Archive 这个牌组及其子牌组的参数。大家可以替换成自己要配置的牌组。如果不够用，请自行复制添加。 

const deckParams = [
  {
    // Default parameters of FSRS4Anki for global
    &#34;deckName&#34;: &#34;global config for FSRS4Anki&#34;,
    &#34;w&#34;: [1, 1, 5, -0.5, -0.5, 0.2, 1.4, -0.12, 0.8, 2, -0.2, 0.2, 1],
    // The above parameters can be optimized via FSRS4Anki optimizer.
    // For details about the parameters, please see: https://github.com/open-spaced-repetition/fsrs4anki/wiki/Free-Spaced-Repetition-Scheduler
    // User&#39;s custom parameters for global
    &#34;requestRetention&#34;: 0.9, // recommended setting: 0.8 ~ 0.9
    &#34;maximumInterval&#34;: 36500,
    &#34;easyBonus&#34;: 1.3,
    &#34;hardInterval&#34;: 1.2,
    // FSRS only modifies the long-term scheduling. So (re)learning steps in deck options work as usual.
    // I recommend setting steps shorter than 1 day.
  },
  {
    // Example 1: User&#39;s custom parameters for this deck and its sub-decks.
    // Need to add  to your card&#39;s front template&#39;s first line.
    &#34;deckName&#34;: &#34;ALL::Learning::English::Reading&#34;,
    &#34;w&#34;: [1.1475, 1.401, 5.1483, -1.4221, -1.2282, 0.035, 1.4668, -0.1286, 0.7539, 1.9671, -0.2307, 0.32, 0.9451],
    &#34;requestRetention&#34;: 0.9,
    &#34;maximumInterval&#34;: 36500,
    &#34;easyBonus&#34;: 1.3,
    &#34;hardInterval&#34;: 1.2,
  },
  {
    // Example 2: User&#39;s custom parameters for this deck and its sub-decks.
    // Don&#39;t omit any keys.
    &#34;deckName&#34;: &#34;ALL::Archive&#34;,
    &#34;w&#34;: [1.2879, 0.5135, 4.9532, -1.502, -1.0922, 0.0081, 1.3771, -0.0294, 0.6718, 1.8335, -0.4066, 0.7291, 0.5517],
    &#34;requestRetention&#34;: 0.9,
    &#34;maximumInterval&#34;: 36500,
    &#34;easyBonus&#34;: 1.3,
    &#34;hardInterval&#34;: 1.2,
  }
];
如果你有些牌组不想使用 FSRS，可以把这些牌组的名称填入 skip_decks 的列表中。

const skip_decks = [&#34;ALL::Learning::ML::NNDL&#34;, &#34;ALL::Learning::English&#34;];
## 3 使用助手插件

Helper 插件纯属锦上添花，不建议过多使用。安装地址：

[FSRS4Anki Helper - AnkiWeb](https://link.zhihu.com/?target=https%3A//ankiweb.net/shared/info/759844606)### 3.1 重新调度

重新调度所有卡片，可以基于前面我们填入的个性化参数，根据每张卡片的复习历史，重新预测记忆状态，并安排间隔。

注意：对于已经使用 Anki 默认算法复习过多次的卡片，重新调度可能会给出与 Scheduler 不同的间隔，因为 Scheduler 在运行时无法获得完整的复习历史。此时重新调度给出的间隔会更加准确。但之后两者就没有区别了。

![](https://pic2.zhimg.com/v2-ca1de143fd11e4fafcd517d29b433991_1440w.jpg)
### 3.2 压力平衡

开启压力平衡选项后，重新规划时会让每天的复习量尽可能一致、平滑。

![](https://pic3.zhimg.com/v2-f4b0644f72dad3f50c38966a925be532_1440w.jpg)
下面是对比，第一张是开之前进行重新调度，第二张是开之后进行重新调度：

![](https://pica.zhimg.com/v2-ecc44145f32f8fc144a287cfe455aee0_1440w.jpg)

![](https://pic2.zhimg.com/v2-7f584c1292ed677639f0e919957534af_1440w.jpg)
### 3.3 周末放假

实际上可以选择在周一到周天任何几天进行放假。开启后，进行重新调度时，Helper 将尽可能避开你设定的日期安排复习。

![](https://pic1.zhimg.com/v2-26d0ab4c33021e9bea30374094c893be_1440w.jpg)
效果：

![](https://picx.zhimg.com/v2-54fbb34bf8abc478d7db58490fb1fe59_1440w.jpg)
### 3.4 提前/推迟

这两个功能很相似，放一起说。你可以设置提前/推迟的卡片数量，Helper 插件将按照相对提前/推迟顺序排序，然后进行提前/推迟，确保在满足你设置的卡片数量的同时，最小化对原有复习安排的偏离。

![](https://pica.zhimg.com/v2-707d07977a3d88e06f5544a6a40b44f6_1440w.jpg)

![](https://pic2.zhimg.com/v2-02732f2010394a33ece76a055f9b3b21_1440w.jpg)
### 3.5 分散关联卡片

在 Anki 中，有些模板会从同一条笔记中生成多张在内容上有关联的卡片，比如翻转卡片（中->英，英->中）和填空卡（当你在同一条笔记上挖了好多个空时）。这些卡片的复习日期如果隔得太近，可能会相互干扰或提醒，关联卡片分散可以让这些卡片的复习日期尽可能错开。

![](https://pic2.zhimg.com/v2-aa5adaca683e7ec7ba67dccac91ecad9_1440w.jpg)
### 3.6 高级搜索

在卡片浏览器中，你可以右键**表头**，点击 Difficulty、Stability、Retention，让卡片浏览器显示卡片当前的记忆状态。

![](https://pic4.zhimg.com/v2-b2b40c84f58f47fbb789c70635732d0f_1440w.jpg)
同时支持三种属性的筛选语法，以下是一些例子：

sd=5：难度等于 5 的卡片
r以上就是 FSRS4Anki 的完整食用指南了，希望对你有所帮助。如果我的工作对你的学习有益，还恳请给我的开源项目 star，给插件页面点赞。

[GitHub - open-spaced-repetition/fsrs4anki: A modern Anki custom scheduling based on free spaced repetition scheduler algorithm](https://link.zhihu.com/?target=https%3A//github.com/open-spaced-repetition/fsrs4anki)[FSRS4Anki Helper - AnkiWeb](https://link.zhihu.com/?target=https%3A//ankiweb.net/shared/info/759844606)
