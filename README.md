<h1>SG-Toolkit</h1>
<p>使用科技手段对抗形式主义，提供了一些自动化脚本。能够帮助你完成网上学堂刷课、安全知识考试自动答题，等</p>
<h2>怎么用？</h2>
<h3>网上学堂刷课</h3>
<pre>
browser = FuckGWXT(
    "san.zhang",
    "1q2w!Q@W",
    "美国能源",
    "http://localhost/www/command/CollegeControl?flag=collegeTC&tcID=ef8afbf81de&tab=collTcLesson&type=&worktypeid=&pageNo1=15&pageSize1=10&comewho=null"
)
browser.run()
</pre>
<h3>安全知识答题</h3>
<h4>代码示例</h4>
<pre>
browser = FuckAnGui(
    "san.zhang",
    "1qaz@WSX",
    "http://localhost/comlogin/routeLogin.html",
    "./题库.xlsx"
)
browser.run()
</pre>
<h4>题库格式</h4>
<table>
<tr>
<th>题型</th><th>题干</th><th>选项</th><th>答案</th>
</tr>
<tr>
<td>单选题</td><td>你今天吃的什么早点？</td><td>A-豆浆|B-八宝粥|C-胡辣汤|D-肉夹馍</td><td>A</td>
</tr>
<tr>
<td>多选题</td><td>你今天吃的什么早点？</td><td>A-豆浆|B-八宝粥|C-胡辣汤|D-肉夹馍</td><td>BCD</td>
</tr>
<tr>
<td>判断题</td><td>今天的早点有豆浆</td><td>A-正确|B-错误</td><td>A</td>
</tr>
</table>
<ol>
<li>表格必须包含<b>题型</b>、<b>题干</b>、<b>选项</b>、<b>答案</b>四列</li>
<li><b>题型</b>只能包含<b>单选题</b>、<b>多选题</b>、<b>判断题</b></li>
<li>每个<b>选项</b>使用单竖线<b>|</b>分隔，并且按照<b>A-选项</b>类似格式书写。<b>判断题</b>选项内容固定为<b>A-正确|B-错误</b></li>
<li><b>答案</b>列有且仅有大写字母</li>
</ol>
<h4>注意事项</h4>
<p>第一次运行程序必定失败，在弹出的窗口输入用户名、密码、验证码，点击登录，浏览器将自动保存登录信息。下次运行即可自动答题。</p>
<h2>环境要求</h2>
<ul>
<li>Chrome浏览器</li>
<li>Chrome WebDriver（版本需与浏览器保持一致）</li>
<li>Python</li>
<li>Python第三方库（见<a href="requirements.txt" target="_blank">requirements.txt</a>）</li>
</ul>
<h2>更新日志</h2>
<table>
<tr>
<th>版本号</th><th>更新内容</th><th>更新日期</th>
</tr>
<tr>
<td>0.1.0</td><td>初始化项目</td><td>2026年7月13日</td>
</tr>
<tr>
<td>0.2.0</td><td>项目更名为SG-Toolkit</td><td>2026年7月14日</td>
</tr>
<tr>
<td>0.2.1</td><td>修复安全知识答题截止到99题的BUG</td><td>2026年7月14日</td>
</tr>
<tr>
<td>0.2.2</td><td>安全知识自动答题完成后显示成绩</td><td>2026年7月14日</td>
</tr>
<tr>
<td>0.2.3</td><td>In sg_toolkit.gkpt.FuckAnGui change Chrome user-data-dir to use current working directory (os.getcwd()) for per-user cache. Replace fragile regex-based bg-size check in exam() with a deterministic counter loop (i from 0 to 99) and increment it each iteration to avoid potential infinite loops while keeping existing submit behavior.</td><td>2026年7月14日</td>
</tr>
<tr>
<td>0.2.4</td><td>Refactor sg_toolkit.gkpt: remove unused re import, add tqdm, replace fragile while/regex loop with a deterministic tqdm(range(100)) loop, make exam() return the page body text and have process() return that result. Update sg_toolkit.gwxt: add module docstring/encoding and make process() return the result of learn().</td><td>2026年7月14日</td>
</tr>
<tr>
<td>0.3.0</td><td>添加注释; 安全知识自动答题工具新增题目数量参数; 启动方法改为<code>browser.run()</code></td><td>2026年7月14日</td>
</tr>
<tr>
<td>0.3.1</td><td>Unpin requirements (requirements.txt), bump package version to 0.3.1 (sg_toolkit/__init__.py). Improve gkpt.py robustness by reading Excel as strings, normalizing whitespace in题型/题干/选项/答案, stripping UI text, replacing prints with logging, trimming option text before matching, and adding explicit ValueError cases for unsupported question types and invalid judge answers. These changes reduce brittle string-matching and improve error visibility.</td><td>2026年7月15日</td>
</tr>
<tr>
<td>0.3.2</td><td>填充题库缺失值为空字符串</td><td>2026年7月21日</td>
</tr>
</table>