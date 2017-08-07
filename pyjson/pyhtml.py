# -*- coding: utf-8 -*-


def tokenize(str_in):
    str_list = html_list(str_in)
    return str_list

def html_list(str_in, index=0, symbol=('<', '>', ' ', '/', '=', '!', )):
    """Returns a list from html parser consumes."""
    T1, T2, SP, SC, KV, SD = symbol
    ret_list = []
    lf = str_in.find(T1 , index)
    while lf >= index:
        nf = str_in.find(T2, lf)
        if lf>nf:
            break
        ret_obj, index = get_mark(str_in, lf, nf, symbol)
        lf = str_in.find(T1, index)
        if ret_obj:
            ret_list.append(ret_obj)
    return ret_list

def get_mark(str_in, ia, ib, symbol):
    T1, T2, SP, SC, KV, SD = symbol
    ret_obj = {"_ia":ia,"_ib":ib}  ## str_in[ia:ib+1]=<...>
    i_tag, i_sc = _skip(str_in, ia+1), str_in.rfind(SC, ia, ib)
    if ia<i_sc<ib and str_in[i_tag]==SC:
        ret_obj["_isc"] = 2   ## 2:like </div>
        ret_obj["_tag"] = str_in[i_sc+1:ib].strip()
    elif str_in[i_tag]==SD:
        ret_obj["_isc"] = 4   ## 2:like <!...>
        ret_obj["_tag"] = str_in[i_tag+1:ib].strip()
    else:
        ret_obj["_isc"] = 3 if ia<i_sc<ib and _skip(str_in, i_sc+1)==ib else 1
        ## 3:like <img .../>, 1:other <...>
        i_attr_end = i_sc if ret_obj["_isc"] == 3 else ib
        i_attr_start = str_in.find(SP, i_tag)
        if i_tag<i_attr_start<i_attr_end:
            ret_obj["_tag"] = str_in[i_tag:i_attr_start].strip()
            str_attr = str_in[i_attr_start+1:i_attr_end].strip()
            if str_attr:
                ret_obj["_attr"] = str_attr
                ret_obj["attr"] = get_attr(str_attr, SP, KV)
        else:
            ret_obj["_tag"] = str_in[i_tag:i_attr_end].strip()

    return (ret_obj, ib+1)

def get_attr(str_in, SP, KV, index=0):
    ret_obj = {}
    ll = len(str_in)
    while index < ll-1:
        ks_list, vs, index = get_kv(str_in, index, ll, SP, KV)
        for ks in ks_list:
            ret_obj[ks] = vs
    return ret_obj

def get_kv(str_in, index, ll, SP, KV):
    ks_list = []
    ks, index = get_block(str_in, index, ll, SP, KV)
    if ks:
        ks_list.append(ks)
    vs, index = get_block(str_in, index+1, ll, SP, KV) if str_in[index] == KV else (ks, index)
    while index<ll and str_in[index] == KV:
        if vs:
            ks_list.append(vs)
        vs, index = get_block(str_in, index+1, ll, SP, KV)
    return (ks_list, vs, index)

def get_block(str_in, index, ll, SP, KV, T="\\", STR={'"':1, "'":1, }):
    index = _skip(str_in, index)
    while str_in[index] == KV and index<ll-1:
        index = _skip(str_in, index+1)
    if index>=ll:
        return (None, ll)
    oi, tc, si, ki = index, str_in[index], str_in.find(SP, index), str_in.find(KV, index)
    if tc in STR:
        while not str_in[index+1] == tc:
            index += 2 if  str_in[index] == T else 1
        ret_str, index = str_in[oi+1:index+1], index+2
    elif index<si and (si<ki or ki<0):
        ret_str, index = str_in[oi:si], si
    elif index<ki and ( si>ki or si<0):
        ret_str, index = str_in[oi:ki], ki
    else:
        ret_str, index = str_in[index:], ll
    return (ret_str, index)

def _skip(str_in, index, B={' ':1, '\r':1, '\n':1, '\t':1, }):
    while str_in[index] in B:
        index += 1
    return index


def parse(html_obj):
    ret_print = {"_ia":1,"_ib":1, "_isc":1, "_tag":1, "_attr":0, "attr":1}
    _print_obj = [{k:v for k,v in i.items() if ret_print.get(k,0)} for i in html_obj]

    _inlen = len(_print_obj)
    print_obj = fix_list(_print_obj, _inlen)

    inlen = len(print_obj)
    ret, index = tree(print_obj, inlen, 0)

    if not index==inlen:
        raise EOFError('error end at %r!' % (print_obj[index:],))
    return ret

def main(str_in):
    html_str = str_in
    html_obj = tokenize(html_str)
    ret = parse(html_obj)


    import json
    msg = json.dumps(ret, ensure_ascii=False, indent=4)

    with open('html.html', 'w') as ff:
        ff.write(html_str)

    with open('html.json', 'w') as ff:
        ff.write(msg)


def fix_list(html_list, list_len, index = 0):
    getit = lambda i:(html_list[i], html_list[i]["_isc"], html_list[i]["_tag"],)
    ret_list, tags = [], []
    while index<list_len:
        item, isc, tag = getit(index)
        if isc==1:
            ret_list.append(item)
            tags.append(tag)
        elif isc==2:
            if tags and tags[-1]==tag:
                ret_list.append(item)
                tags.pop()
            elif tags:
                ret_list.append({"_ia":0,"_ib":0, "_isc":2, "_tag":tags[-1],})
                tags.pop()
                continue
            else:
                ret_list.append({"_ia":0,"_ib":0, "_isc":1, "_tag":tag,})
                ret_list.append(item)
        else:
            ret_list.append(item)
        index += 1
    return ret_list

def tree(html_list, list_len, index=0, nfind=None):
    ret = []
    getit = lambda i:(html_list[i], html_list[i]["_isc"], html_list[i]["_tag"],)
    while index<list_len:
        item, isc, tag = getit(index)
        if isc==1:
            tmp, index = tree(html_list, list_len, index+1, nfind=tag)
            if tmp:
                item['_sub'] = tmp
            _item, _isc, _tag = getit(index)
            if not _tag==tag:
                raise EOFError('list not match at %r:%r!' % (item, _item))
            item['_ic'], item['_id'] = _item['_ia'], _item['_ib']
            ret.append(item)
        elif isc==2:
            if nfind==tag:
                break
        elif isc==3:
            ret.append(item)
        index += 1
    return ret, index

if __name__=="__main__":
    print 'test start'
    str_t = """
<div class="entry">


		<div class="copyright-area">本文由 <a href="http://python.jobbole.com">伯乐在线</a> - <a href="http://www.jobbole.com/members/pyper">PyPer</a> 翻译，<a href="http://www.jobbole.com/members/daetalus">Daetalus</a> 校稿。未经许可，禁止转载！<br>英文出处：<a target="_blank" href="http://www.enotagain.com/essays/how-to-implement-a-type-checker-in-python-3.html">www.enotagain.com</a>。欢迎加入<a target="_blank" href="http://group.jobbole.com/category/feedback/trans-team/">翻译组</a>。</div><p><span style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-style: normal; font-weight: bold; line-height: 36px;">示例函数</span></p>
<p>为了开发类型检查器，我们需要一个简单的函数对其进行实验。欧几里得算法就是一个完美的例子：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a717502812450" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码" style="display: none;"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">def gcd(a, b):
    '''Return the greatest common divisor of a and b.'''
    a = abs(a)
    b = abs(b)
    if a &lt; b:
        a, b = b, a
    while b != 0:
        a, b = b, a % b
    return a</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a717502812450-1">1</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a717502812450-2">2</div><div class="crayon-num" data-line="crayon-5612a14b1a717502812450-3">3</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a717502812450-4">4</div><div class="crayon-num" data-line="crayon-5612a14b1a717502812450-5">5</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a717502812450-6">6</div><div class="crayon-num" data-line="crayon-5612a14b1a717502812450-7">7</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a717502812450-8">8</div><div class="crayon-num" data-line="crayon-5612a14b1a717502812450-9">9</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a717502812450-1"><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">gcd</span><span class="crayon-sy">(</span><span class="crayon-v">a</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">b</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a717502812450-2"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-s">'''Return the greatest common divisor of a and b.'''</span></div><div class="crayon-line" id="crayon-5612a14b1a717502812450-3"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">a</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-k ">abs</span><span class="crayon-sy">(</span><span class="crayon-v">a</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a717502812450-4"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">b</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-k ">abs</span><span class="crayon-sy">(</span><span class="crayon-v">b</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a717502812450-5"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-v">a</span><span class="crayon-h"> </span><span class="crayon-o">&lt;</span><span class="crayon-h"> </span><span class="crayon-v">b</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a717502812450-6"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">a</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">b</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">b</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-i">a</span></div><div class="crayon-line" id="crayon-5612a14b1a717502812450-7"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">while</span><span class="crayon-h"> </span><span class="crayon-v">b</span><span class="crayon-h"> </span><span class="crayon-o">!=</span><span class="crayon-h"> </span><span class="crayon-cn">0</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a717502812450-8"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">a</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">b</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">b</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">a</span><span class="crayon-h"> </span><span class="crayon-o">%</span><span class="crayon-h"> </span><span class="crayon-i">b</span></div><div class="crayon-line" id="crayon-5612a14b1a717502812450-9"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-v">a</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0037 seconds] -->
<p>在上面的示例中，参数 a 和 b 以及返回值应该是 int 类型的。预期的类型将会以函数注解的形式来表达，函数注解是 Python 3 的一个新特性。接下来，类型检查机制将会以一个装饰器的形式实现，注解版本的第一行代码是：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a725299012817" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码" style="display: none;"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">def gcd(a: int, b: int) -&gt; int:</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a725299012817-1">1</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a725299012817-1"><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">gcd</span><span class="crayon-sy">(</span><span class="crayon-v">a</span><span class="crayon-o">:</span><span class="crayon-h"> </span><span class="crayon-k ">int</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">b</span><span class="crayon-o">:</span><span class="crayon-h"> </span><span class="crayon-k ">int</span><span class="crayon-sy">)</span><span class="crayon-h"> </span><span class="crayon-o">-&gt;</span><span class="crayon-h"> </span><span class="crayon-k ">int</span><span class="crayon-o">:</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0011 seconds] -->
<p>使用“gcd.__annotations__”可以获得一个包含注解的字典：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a72b609993341" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码" style="display: none;"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">&gt;&gt;&gt; gcd.__annotations__
{'return': &lt;class 'int'&gt;, 'b': &lt;class 'int'&gt;, 'a': &lt;class 'int'&gt;}
&gt;&gt;&gt; gcd.__annotations__['a']
&lt;class 'int'&gt;</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a72b609993341-1">1</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a72b609993341-2">2</div><div class="crayon-num" data-line="crayon-5612a14b1a72b609993341-3">3</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a72b609993341-4">4</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a72b609993341-1"><span class="crayon-o">&gt;&gt;&gt;</span><span class="crayon-h"> </span><span class="crayon-v">gcd</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations_</span><span class="crayon-sy">_</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a72b609993341-2"><span class="crayon-sy">{</span><span class="crayon-s">'return'</span><span class="crayon-o">:</span><span class="crayon-h"> </span><span class="crayon-o">&lt;</span><span class="crayon-t">class</span><span class="crayon-h"> </span><span class="crayon-s">'int'</span><span class="crayon-o">&gt;</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-s">'b'</span><span class="crayon-o">:</span><span class="crayon-h"> </span><span class="crayon-o">&lt;</span><span class="crayon-t">class</span><span class="crayon-h"> </span><span class="crayon-s">'int'</span><span class="crayon-o">&gt;</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-s">'a'</span><span class="crayon-o">:</span><span class="crayon-h"> </span><span class="crayon-o">&lt;</span><span class="crayon-t">class</span><span class="crayon-h"> </span><span class="crayon-s">'int'</span><span class="crayon-o">&gt;</span><span class="crayon-sy">}</span></div><div class="crayon-line" id="crayon-5612a14b1a72b609993341-3"><span class="crayon-o">&gt;&gt;&gt;</span><span class="crayon-h"> </span><span class="crayon-v">gcd</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">[</span><span class="crayon-s">'a'</span><span class="crayon-sy">]</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a72b609993341-4"><span class="crayon-o">&lt;</span><span class="crayon-t">class</span><span class="crayon-h"> </span><span class="crayon-s">'int'</span><span class="crayon-o">&gt;</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0023 seconds] -->
<p>需要注意的是，返回值的注解存储在键“return”下。这是有可能的，因为“return”是一个关键字，所以不能用作一个有效的参数名。</p>
<h2>检查返回值类型</h2>
<p>返回值注解存储在字典“__annotations__”中的“return”键下。我们将使用这个值来检查返回值（假设注解存在）。我们将参数传递给原始函数，如果存在注解，我们将通过注解中的值来验证其类型：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a732933477465" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">def typecheck(f):
    def wrapper(*args, **kwargs):
        result = f(*args, **kwargs)
        return_type = f.__annotations__.get('return', None)
        if return_type and not isinstance(result, return_type):
            raise RuntimeError("{} should return {}".format(f.__name__, return_type.__name__))
        return result
    return wrapper</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a732933477465-1">1</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a732933477465-2">2</div><div class="crayon-num" data-line="crayon-5612a14b1a732933477465-3">3</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a732933477465-4">4</div><div class="crayon-num" data-line="crayon-5612a14b1a732933477465-5">5</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a732933477465-6">6</div><div class="crayon-num" data-line="crayon-5612a14b1a732933477465-7">7</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a732933477465-8">8</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a732933477465-1"><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">typecheck</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a732933477465-2"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">wrapper</span><span class="crayon-sy">(</span><span class="crayon-o">*</span><span class="crayon-v">args</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-o">*</span><span class="crayon-o">*</span><span class="crayon-v">kwargs</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a732933477465-3"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">result</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-e">f</span><span class="crayon-sy">(</span><span class="crayon-o">*</span><span class="crayon-v">args</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-o">*</span><span class="crayon-o">*</span><span class="crayon-v">kwargs</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a732933477465-4"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">return_type</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">.</span><span class="crayon-e">get</span><span class="crayon-sy">(</span><span class="crayon-s">'return'</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-t">None</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a732933477465-5"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-e">return_type </span><span class="crayon-st">and</span><span class="crayon-h"> </span><span class="crayon-st">not</span><span class="crayon-h"> </span><span class="crayon-k ">isinstance</span><span class="crayon-sy">(</span><span class="crayon-v">result</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">return_type</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a732933477465-6"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should return {}"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">return_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a732933477465-7"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-e">result</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a732933477465-8"><span class="crayon-e">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-v">wrapper</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0039 seconds] -->
<p>我们可以用“a”替换函数gcd的返回值来测试上面的代码：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a738605956119" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">Traceback (most recent call last):
  File "typechecker.py", line 9, in &lt;module&gt;
    gcd(1, 2)
  File "typechecker.py", line 5, in wrapper
    raise RuntimeError("{} should return {}".format(f.__name__, return_type.__name__))
RuntimeError: gcd should return int</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a738605956119-1">1</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a738605956119-2">2</div><div class="crayon-num" data-line="crayon-5612a14b1a738605956119-3">3</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a738605956119-4">4</div><div class="crayon-num" data-line="crayon-5612a14b1a738605956119-5">5</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a738605956119-6">6</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a738605956119-1"><span class="crayon-k ">Traceback</span><span class="crayon-h"> </span><span class="crayon-sy">(</span><span class="crayon-e">most </span><span class="crayon-e">recent </span><span class="crayon-e">call </span><span class="crayon-v">last</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a738605956119-2"><span class="crayon-h">&nbsp;&nbsp;</span><span class="crayon-k ">File</span><span class="crayon-h"> </span><span class="crayon-s">"typechecker.py"</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-i">line</span><span class="crayon-h"> </span><span class="crayon-cn">9</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-st">in</span><span class="crayon-h"> </span><span class="crayon-o">&lt;</span><span class="crayon-v">module</span><span class="crayon-o">&gt;</span></div><div class="crayon-line" id="crayon-5612a14b1a738605956119-3"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-e">gcd</span><span class="crayon-sy">(</span><span class="crayon-cn">1</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-cn">2</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a738605956119-4"><span class="crayon-h">&nbsp;&nbsp;</span><span class="crayon-k ">File</span><span class="crayon-h"> </span><span class="crayon-s">"typechecker.py"</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-i">line</span><span class="crayon-h"> </span><span class="crayon-cn">5</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-st">in</span><span class="crayon-h"> </span><span class="crayon-e">wrapper</span></div><div class="crayon-line" id="crayon-5612a14b1a738605956119-5"><span class="crayon-e">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should return {}"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">return_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a738605956119-6"><span class="crayon-k ">RuntimeError</span><span class="crayon-o">:</span><span class="crayon-h"> </span><span class="crayon-e">gcd </span><span class="crayon-e">should </span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-k ">int</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0031 seconds] -->
<p>由上面的结果可知，确实检查了返回值的类型。</p>
<h2><span style="font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; font-size: 24px; font-style: normal; font-weight: bold; line-height: 36px;">检查参数类型</span></h2>
<p>函数的参数存在于关联代码对象的“co_varnames”属性中，在我们的例子中是“gcd.__code__.co_varnames”。元组包含了所有局部变量的名称，并且该元组以参数开始，参数数量存储在“co_nlocals”中。我们需要遍历包括索引在内的所有变量，并从参数“args”中获取参数值，最后对其进行类型检查。</p>
<p>得到了下面的代码：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a73e181686909" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">def typecheck(f):
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args[:f.__code__.co_nlocals]):
            name = f.__code__.co_varnames[i]
            expected_type = f.__annotations__.get(name, None)
            if expected_type and not isinstance(arg, expected_type):
                raise RuntimeError("{} should be of type {}; {} specified".format(name, expected_type.__name__, type(arg).__name__))
        result = f(*args, **kwargs)
        return_type = f.__annotations__.get('return', None)
        if return_type and not isinstance(result, return_type):
            raise RuntimeError("{} should return {}".format(f.__name__, return_type.__name__))
        return result
    return wrapper</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a73e181686909-1">1</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a73e181686909-2">2</div><div class="crayon-num" data-line="crayon-5612a14b1a73e181686909-3">3</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a73e181686909-4">4</div><div class="crayon-num" data-line="crayon-5612a14b1a73e181686909-5">5</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a73e181686909-6">6</div><div class="crayon-num" data-line="crayon-5612a14b1a73e181686909-7">7</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a73e181686909-8">8</div><div class="crayon-num" data-line="crayon-5612a14b1a73e181686909-9">9</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a73e181686909-10">10</div><div class="crayon-num" data-line="crayon-5612a14b1a73e181686909-11">11</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a73e181686909-12">12</div><div class="crayon-num" data-line="crayon-5612a14b1a73e181686909-13">13</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a73e181686909-1"><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">typecheck</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a73e181686909-2"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">wrapper</span><span class="crayon-sy">(</span><span class="crayon-o">*</span><span class="crayon-v">args</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-o">*</span><span class="crayon-o">*</span><span class="crayon-v">kwargs</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a73e181686909-3"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">for</span><span class="crayon-h"> </span><span class="crayon-v">i</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-e">arg </span><span class="crayon-st">in</span><span class="crayon-h"> </span><span class="crayon-k ">enumerate</span><span class="crayon-sy">(</span><span class="crayon-v">args</span><span class="crayon-sy">[</span><span class="crayon-o">:</span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__code__</span><span class="crayon-sy">.</span><span class="crayon-v">co_nlocals</span><span class="crayon-sy">]</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a73e181686909-4"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">name</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__code__</span><span class="crayon-sy">.</span><span class="crayon-v">co_varnames</span><span class="crayon-sy">[</span><span class="crayon-v">i</span><span class="crayon-sy">]</span></div><div class="crayon-line" id="crayon-5612a14b1a73e181686909-5"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">expected_type</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">.</span><span class="crayon-e">get</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-t">None</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a73e181686909-6"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-e">expected_type </span><span class="crayon-st">and</span><span class="crayon-h"> </span><span class="crayon-st">not</span><span class="crayon-h"> </span><span class="crayon-k ">isinstance</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a73e181686909-7"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should be of type {}; {} specified"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-k ">type</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">)</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a73e181686909-8"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">result</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-e">f</span><span class="crayon-sy">(</span><span class="crayon-o">*</span><span class="crayon-v">args</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-o">*</span><span class="crayon-o">*</span><span class="crayon-v">kwargs</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a73e181686909-9"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">return_type</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">.</span><span class="crayon-e">get</span><span class="crayon-sy">(</span><span class="crayon-s">'return'</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-t">None</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a73e181686909-10"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-e">return_type </span><span class="crayon-st">and</span><span class="crayon-h"> </span><span class="crayon-st">not</span><span class="crayon-h"> </span><span class="crayon-k ">isinstance</span><span class="crayon-sy">(</span><span class="crayon-v">result</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">return_type</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a73e181686909-11"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should return {}"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">return_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a73e181686909-12"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-e">result</span></div><div class="crayon-line" id="crayon-5612a14b1a73e181686909-13"><span class="crayon-e">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-v">wrapper</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0070 seconds] -->
<p>在上面的循环中，i是数组args中参数的以0起始的索引，arg是包含其值的字符串。可以利用“f.__code__.co_varnames[i]”读取到参数的名称。类型检查代码与返回值类型检查完全一样（包括错误消息的异常）。</p>
<p>为了对关键字参数进行类型检查，我们需要遍历参数kwargs。此时的类型检查几乎与第一个循环中相同：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a744885501159" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">for name, arg in kwargs.items():
    expected_type = f.__annotations__.get(name, None)
    if expected_type and not isinstance(arg, expected_type):
        raise RuntimeError("{} should be of type {}; {} specified".format(name, expected_type.__name__, type(arg).__name__))</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a744885501159-1">1</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a744885501159-2">2</div><div class="crayon-num" data-line="crayon-5612a14b1a744885501159-3">3</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a744885501159-4">4</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a744885501159-1"><span class="crayon-st">for</span><span class="crayon-h"> </span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-e">arg </span><span class="crayon-st">in</span><span class="crayon-h"> </span><span class="crayon-v">kwargs</span><span class="crayon-sy">.</span><span class="crayon-e">items</span><span class="crayon-sy">(</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a744885501159-2"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">expected_type</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">.</span><span class="crayon-e">get</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-t">None</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a744885501159-3"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-e">expected_type </span><span class="crayon-st">and</span><span class="crayon-h"> </span><span class="crayon-st">not</span><span class="crayon-h"> </span><span class="crayon-k ">isinstance</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a744885501159-4"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should be of type {}; {} specified"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-k ">type</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">)</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0029 seconds] -->
<p>得到的装饰器代码如下：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a74a224274838" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">def typecheck(f):
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args[:f.__code__.co_nlocals]):
            name = f.__code__.co_varnames[i]
            expected_type = f.__annotations__.get(name, None)
            if expected_type and not isinstance(arg, expected_type):
                raise RuntimeError("{} should be of type {}; {} specified".format(name, expected_type.__name__, type(arg).__name__))
        for name, arg in kwargs.items():
            expected_type = f.__annotations__.get(name, None)
            if expected_type and not isinstance(arg, expected_type):
                raise RuntimeError("{} should be of type {}; {} specified".format(name, expected_type.__name__, type(arg).__name__))
        result = f(*args, **kwargs)
        return_type = f.__annotations__.get('return', None)
        if return_type and not isinstance(result, return_type):
            raise RuntimeError("{} should return {}".format(f.__name__, return_type.__name__))
        return result
    return wrapper</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-1">1</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a74a224274838-2">2</div><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-3">3</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a74a224274838-4">4</div><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-5">5</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a74a224274838-6">6</div><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-7">7</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a74a224274838-8">8</div><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-9">9</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a74a224274838-10">10</div><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-11">11</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a74a224274838-12">12</div><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-13">13</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a74a224274838-14">14</div><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-15">15</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a74a224274838-16">16</div><div class="crayon-num" data-line="crayon-5612a14b1a74a224274838-17">17</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a74a224274838-1"><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">typecheck</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a74a224274838-2"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">wrapper</span><span class="crayon-sy">(</span><span class="crayon-o">*</span><span class="crayon-v">args</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-o">*</span><span class="crayon-o">*</span><span class="crayon-v">kwargs</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a74a224274838-3"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">for</span><span class="crayon-h"> </span><span class="crayon-v">i</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-e">arg </span><span class="crayon-st">in</span><span class="crayon-h"> </span><span class="crayon-k ">enumerate</span><span class="crayon-sy">(</span><span class="crayon-v">args</span><span class="crayon-sy">[</span><span class="crayon-o">:</span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__code__</span><span class="crayon-sy">.</span><span class="crayon-v">co_nlocals</span><span class="crayon-sy">]</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a74a224274838-4"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">name</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__code__</span><span class="crayon-sy">.</span><span class="crayon-v">co_varnames</span><span class="crayon-sy">[</span><span class="crayon-v">i</span><span class="crayon-sy">]</span></div><div class="crayon-line" id="crayon-5612a14b1a74a224274838-5"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">expected_type</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">.</span><span class="crayon-e">get</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-t">None</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a74a224274838-6"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-e">expected_type </span><span class="crayon-st">and</span><span class="crayon-h"> </span><span class="crayon-st">not</span><span class="crayon-h"> </span><span class="crayon-k ">isinstance</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a74a224274838-7"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should be of type {}; {} specified"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-k ">type</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">)</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a74a224274838-8"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">for</span><span class="crayon-h"> </span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-e">arg </span><span class="crayon-st">in</span><span class="crayon-h"> </span><span class="crayon-v">kwargs</span><span class="crayon-sy">.</span><span class="crayon-e">items</span><span class="crayon-sy">(</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a74a224274838-9"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">expected_type</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">.</span><span class="crayon-e">get</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-t">None</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a74a224274838-10"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-e">expected_type </span><span class="crayon-st">and</span><span class="crayon-h"> </span><span class="crayon-st">not</span><span class="crayon-h"> </span><span class="crayon-k ">isinstance</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a74a224274838-11"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should be of type {}; {} specified"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-k ">type</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">)</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a74a224274838-12"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">result</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-e">f</span><span class="crayon-sy">(</span><span class="crayon-o">*</span><span class="crayon-v">args</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-o">*</span><span class="crayon-o">*</span><span class="crayon-v">kwargs</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a74a224274838-13"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">return_type</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">.</span><span class="crayon-e">get</span><span class="crayon-sy">(</span><span class="crayon-s">'return'</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-t">None</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a74a224274838-14"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-e">return_type </span><span class="crayon-st">and</span><span class="crayon-h"> </span><span class="crayon-st">not</span><span class="crayon-h"> </span><span class="crayon-k ">isinstance</span><span class="crayon-sy">(</span><span class="crayon-v">result</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">return_type</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a74a224274838-15"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should return {}"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">return_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a74a224274838-16"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-e">result</span></div><div class="crayon-line" id="crayon-5612a14b1a74a224274838-17"><span class="crayon-e">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-v">wrapper</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0098 seconds] -->
<p>将类型检查代码写成一个函数将会使代码更加清晰。为了简化代码，我们修改错误信息，而当返回值是无效的类型时，将会使用到这些错误信息。我们也可以利用 functools 模块中的 wraps 方法，将包装函数的一些属性复制到 wrapper 中（这使得 wrapper 看起来更像原来的函数）：</p><!-- Crayon Syntax Highlighter v2.7.1 -->

		<div id="crayon-5612a14b1a750577360341" class="crayon-syntax crayon-theme-github crayon-font-monaco crayon-os-pc print-yes notranslate" data-settings=" touchscreen minimize scroll-mouseover" style="margin-top: 12px; margin-bottom: 12px; font-size: 13px !important; line-height: 15px !important; height: auto;">

			<div class="crayon-toolbar" data-settings=" show" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><span class="crayon-title"></span>
			<div class="crayon-tools" style="font-size: 13px !important;height: 19.5px !important; line-height: 19.5px !important;"><div class="crayon-button crayon-nums-button crayon-pressed" title="切换是否显示行编号"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-plain-button" title="纯文本显示代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-wrap-button" title="切换自动换行"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-expand-button" title="点击展开代码"><div class="crayon-button-icon"></div></div><div class="crayon-button crayon-popup-button" title="在新窗口中显示代码"><div class="crayon-button-icon"></div></div><span class="crayon-language">Python</span></div></div>
			<div class="crayon-info" style="min-height: 18.2px !important; line-height: 18.2px !important;"></div>
			<div class="crayon-plain-wrap"><textarea wrap="soft" class="crayon-plain print-no" data-settings="dblclick" style="tab-size: 4; font-size: 13px !important; line-height: 15px !important; z-index: 0; opacity: 0;">def typecheck(f):
    def do_typecheck(name, arg):
        expected_type = f.__annotations__.get(name, None)
        if expected_type and not isinstance(arg, expected_type):
            raise RuntimeError("{} should be of type {} instead of {}".format(name, expected_type.__name__, type(arg).__name__))

    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        for i, arg in enumerate(args[:f.__code__.co_nlocals]):
            do_typecheck(f.__code__.co_varnames[i], arg)
        for name, arg in kwargs.items():
            do_typecheck(name, arg)

        result = f(*args, **kwargs)

        do_typecheck('return', result)
        return result
    return wrapper</textarea></div>
			<div class="crayon-main" style="position: relative; z-index: 1;">
				<table class="crayon-table" style="">
					<tbody><tr class="crayon-row">
				<td class="crayon-nums " data-settings="show">
					<div class="crayon-nums-content" style="font-size: 13px !important; line-height: 15px !important;"><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-1">1</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-2">2</div><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-3">3</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-4">4</div><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-5">5</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-6">6</div><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-7">7</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-8">8</div><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-9">9</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-10">10</div><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-11">11</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-12">12</div><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-13">13</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-14">14</div><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-15">15</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-16">16</div><div class="crayon-num" data-line="crayon-5612a14b1a750577360341-17">17</div><div class="crayon-num crayon-striped-num" data-line="crayon-5612a14b1a750577360341-18">18</div></div>
				</td>
						<td class="crayon-code"><div class="crayon-pre" style="font-size: 13px !important; line-height: 15px !important; -moz-tab-size:4; -o-tab-size:4; -webkit-tab-size:4; tab-size:4;"><div class="crayon-line" id="crayon-5612a14b1a750577360341-1"><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">typecheck</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-2"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">do_typecheck</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">arg</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a750577360341-3"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">expected_type</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__annotations__</span><span class="crayon-sy">.</span><span class="crayon-e">get</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-t">None</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-4"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">if</span><span class="crayon-h"> </span><span class="crayon-e">expected_type </span><span class="crayon-st">and</span><span class="crayon-h"> </span><span class="crayon-st">not</span><span class="crayon-h"> </span><span class="crayon-k ">isinstance</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a750577360341-5"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">raise</span><span class="crayon-h"> </span><span class="crayon-k ">RuntimeError</span><span class="crayon-sy">(</span><span class="crayon-s">"{} should be of type {} instead of {}"</span><span class="crayon-sy">.</span><span class="crayon-k ">format</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">expected_type</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-k ">type</span><span class="crayon-sy">(</span><span class="crayon-v">arg</span><span class="crayon-sy">)</span><span class="crayon-sy">.</span><span class="crayon-v">__name__</span><span class="crayon-sy">)</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-6">&nbsp;</div><div class="crayon-line" id="crayon-5612a14b1a750577360341-7"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-sy">@</span><span class="crayon-k ">functools</span><span class="crayon-sy">.</span><span class="crayon-e">wraps</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">)</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-8"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-r">def</span><span class="crayon-h"> </span><span class="crayon-e">wrapper</span><span class="crayon-sy">(</span><span class="crayon-o">*</span><span class="crayon-v">args</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-o">*</span><span class="crayon-o">*</span><span class="crayon-v">kwargs</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line" id="crayon-5612a14b1a750577360341-9"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">for</span><span class="crayon-h"> </span><span class="crayon-v">i</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-e">arg </span><span class="crayon-st">in</span><span class="crayon-h"> </span><span class="crayon-k ">enumerate</span><span class="crayon-sy">(</span><span class="crayon-v">args</span><span class="crayon-sy">[</span><span class="crayon-o">:</span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__code__</span><span class="crayon-sy">.</span><span class="crayon-v">co_nlocals</span><span class="crayon-sy">]</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-10"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-e">do_typecheck</span><span class="crayon-sy">(</span><span class="crayon-v">f</span><span class="crayon-sy">.</span><span class="crayon-v">__code__</span><span class="crayon-sy">.</span><span class="crayon-v">co_varnames</span><span class="crayon-sy">[</span><span class="crayon-v">i</span><span class="crayon-sy">]</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">arg</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a750577360341-11"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">for</span><span class="crayon-h"> </span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-e">arg </span><span class="crayon-st">in</span><span class="crayon-h"> </span><span class="crayon-v">kwargs</span><span class="crayon-sy">.</span><span class="crayon-e">items</span><span class="crayon-sy">(</span><span class="crayon-sy">)</span><span class="crayon-o">:</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-12"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-e">do_typecheck</span><span class="crayon-sy">(</span><span class="crayon-v">name</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">arg</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a750577360341-13">&nbsp;</div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-14"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-v">result</span><span class="crayon-h"> </span><span class="crayon-o">=</span><span class="crayon-h"> </span><span class="crayon-e">f</span><span class="crayon-sy">(</span><span class="crayon-o">*</span><span class="crayon-v">args</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-o">*</span><span class="crayon-o">*</span><span class="crayon-v">kwargs</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a750577360341-15">&nbsp;</div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-16"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-e">do_typecheck</span><span class="crayon-sy">(</span><span class="crayon-s">'return'</span><span class="crayon-sy">,</span><span class="crayon-h"> </span><span class="crayon-v">result</span><span class="crayon-sy">)</span></div><div class="crayon-line" id="crayon-5612a14b1a750577360341-17"><span class="crayon-h">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-e">result</span></div><div class="crayon-line crayon-striped-line" id="crayon-5612a14b1a750577360341-18"><span class="crayon-e">&nbsp;&nbsp;&nbsp;&nbsp;</span><span class="crayon-st">return</span><span class="crayon-h"> </span><span class="crayon-v">wrapper</span></div></div></td>
					</tr>
				</tbody></table>
			</div>
		</div>
<!-- [Format Time: 0.0078 seconds] -->
<p></p>
<h2>结论</h2>
<p>注解是 Python 3 中的一个新元素，本文例子中的使用方法很普通，你也可以想象很多特定领域的应用。虽然上面的实现代码并不能满足实际产品要求，但它的目的本来就是用作概念验证。可以对其进行以下改善：</p>
<ul>
<li>处理额外的参数（ args 中意想不到的项目）</li>
<li>默认值类型检查</li>
<li>支持多个类型</li>
<li>支持模板类型（例如，int 型列表）</li>
</ul>



    <div class="post-adds">
        <span data-post-id="81423" class=" btn-bluet-bigger href-style vote-post-up   register-user-only "><i class="fa  fa-thumbs-o-up"></i> <h10 id="81423votetotal">1</h10> 赞</span>
        <span data-book-type="1" data-site-id="13" data-item-id="81423" data-item-type="1" class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "><i class="fa fa-bookmark-o  "></i>  收藏</span>

                    <a href="#article-comment"><span class="btn-bluet-bigger href-style hide-on-480"><i class="fa fa-comments-o"></i>  评论</span></a>



        <!-- JiaThis Button BEGIN -->
        <div class="jiathis_style_24x24" style="display: inline-flex; position: relative; margin: 0; clear: both;float: right;">
            <a class="jiathis_button_tsina" title="分享到新浪微博"><span class="jiathis_txt jtico jtico_tsina"></span></a>
            <a class="jiathis_button_weixin" title="分享到微信"><span class="jiathis_txt jtico jtico_weixin"></span></a>
            <a class="jiathis_button_qzone" title="分享到QQ空间"><span class="jiathis_txt jtico jtico_qzone"></span></a>
            <a class="jiathis_button_fb hide-on-480" title="分享到Facebook"><span class="jiathis_txt jtico jtico_fb"></span></a>
            <a href="http://www.jiathis.com/share?uid=1745061" class="jiathis jiathis_txt jiathis_separator jtico jtico_jiathis" target="_blank"></a>
        </div>

    </div>




        <!-- BEGIN #author-bio -->

<div id="author-bio">

	<h3 class="widget-title">
	关于作者：<a target="_blank" href="http://www.jobbole.com/members/pyper">PyPer</a>
	</h3>
	<div class="alignleft">
		<a target="_blank" href="http://www.jobbole.com/members/pyper">
			<img src="http://www.jobbole.com/wp-content/uploads/avatars/49753/195027efcf792d18eb3478ec692d4f65-bpfull.jpg">
		</a>
	</div>

    <div class="author-bio-info">

        <span class="author-bio-info-block">
            一名就读于羊城某高校的学生，主要关注 Python、Perl 等脚本技术，新浪微博：@LIwianwpIO。        </span>
        <span class="author-bio-info-block">
            <a href="http://www.jobbole.com/members/pyper" target="_blank"><i class="fa fa-user"></i> 个人主页</a> ·
            <a href="http://python.jobbole.com/author/pyper/" target="_blank"><i class="fa fa-file-text-o"></i> 我的文章</a>

             · <a title="声望值" target="_blank" href="http://www.jobbole.com/members/pyper/reputation/"><i class="fa fa-graduation-cap"></i> 10</a>        </span>
    </div>
	<div class="clear"></div>
</div>

<!-- END #author-bio -->
	</div>
"""
    main(str_t)
    print 'end'
