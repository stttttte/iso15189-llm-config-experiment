# P0-1 专家盲评工作包

## 文件清单
- `paper_01.md` ~ `paper_10.md`：10 篇待盲评文件（已随机打乱，组信息不可见）
- `rating_sheet.md`：评分表，**请在此文件打分**
- `key.json`：组映射（**评分完成前请勿打开**）
- `compute_icc.py`：评分完成后跑一下，得到 ICC

## 评分流程
1. 依次打开 `paper_01.md` ~ `paper_10.md`，粗读 5-10 分钟
2. 在 `rating_sheet.md` 对应段落填分（0-5 整数，5 维度）
3. 理由可选（省略也行，只要数字）
4. 评分全部完成后告诉 Claude，跑 `python3 compute_icc.py`

## 预计工作量
- 每篇 ~15 分钟，合计 2-3 小时
- 可以分多次完成（不会污染评分）

## 统计对比
评分完成后，ICC 会对比：
- 你 vs Claude judge
- 你 vs GPT judge
- 你 vs 两 judge 均值
- ICC(2,1) 和 ICC(3,1) 双口径
