使用 Python 检查 data 下的每个文件夹中的文件，每个文件夹需要单独检查
文件格式为 {变量名}_day_{模型名}_{模式名}_{批次编号}_gn_{开始时间}-{结束时间}.clipped.nc
首先将所有同一变量、同一模型、同一模式、同一批次编号的文件进行归类，查看整体的开始时间和结束时间，查看是否有缺失数据，如果有缺失数据，则输出缺失数据的时间范围。

检查条件如下：
1. 变量有 hur、pr、rsds、sfcWind、tas、tasmin、tasmax
2. 模型有 ACCESS-CM2,ACCESS-ESM1-5,BCC-CSM2-MR,CanESM5,EC-Earth3,FGOALS-g3,INM-CM4-8,INM-CM5-0,IPSL-CM6A-LR,KACE-1-0-G,MIROC6,MIROC-ES2L,MPI-ESM1-2-HR,MRI-ESM2-0,NorESM2-MM,UKESM1-0-LL
3. 模式有 historical,ssp126,ssp245,ssp370,ssp585
4. 批次编号可以任意取
5. 模式为 historical 的文件，需要包含 1950-01-01 到 2014-12-31 的数据
6. 模式为 ssp126,ssp245,ssp370,ssp585 的文件，需要包含 2015-01-01 到 2100-12-31 的数据

将结果输出到一个 csv 文件，每一行代表一个模型，每一列代表变量+模式，如果完成则单元格为空，如果没有完成标记缺失的日期