# 距离信息（共15个节点，wh+14)
import copy
import random
import time

d = [[0, 4287, 4332, 10973, 8991, 15282, 14911, 14911, 5027, 21544, 9181, 10101, 5710, 6684, 7978],
     [4287, 0, 3101, 13933, 12069, 18242, 17871, 17871, 6325, 24504, 12141, 13061, 11728, 3798, 8054],
     [4332, 3101, 0, 12439, 10525, 16773, 16402, 16402, 9169, 22465, 9007, 10841, 9852, 2329, 7222],
     [10973, 13933, 12439, 0, 6539, 13294, 11399, 11399, 15408, 11802, 5451, 2930, 15167, 12493, 7347],
     [8991, 12069, 10525, 6539, 0, 15062, 13167, 13167, 12311, 12976, 1546, 3342, 15512, 5751, 3123],
     [15282, 18242, 16773, 13294, 15062, 0, 5047, 5047, 10894, 22763, 13600, 14454, 7389, 15780, 12965],
     [14911, 17871, 16402, 11399, 13167, 5047, 0, 2910, 13162, 18857, 11333, 12187, 9657, 17984, 13183],
     [14911, 17871, 16402, 11399, 13167, 5047, 2910, 0, 13162, 18857, 11333, 12187, 9657, 17984, 13183],
     [5027, 6325, 9169, 15408, 12311, 10894, 13162, 13162, 0, 25113, 12750, 13670, 4709, 9115, 11547],
     [21544, 24504, 22465, 11802, 12976, 22763, 18857, 18857, 25113, 0, 14066, 10769, 22963, 20090, 15897],
     [9181, 12141, 9007, 5451, 1546, 13600, 11333, 11333, 12750, 14066, 0, 2241, 15649, 8420, 3415],
     [10101, 13061, 10841, 2930, 3342, 14454, 12187, 12187, 13670, 10769, 2241, 0, 16216, 9129, 4617],
     [5710, 11728, 9852, 15167, 15512, 7389, 9657, 9657, 4709, 22963, 15649, 16216, 0, 9408, 15623],
     [6684, 3798, 2329, 12493, 5751, 15780, 17984, 17984, 9115, 20090, 8420, 9129, 9408, 0, 5806],
     [7978, 8054, 7222, 7347, 3123, 12965, 13183, 13183, 11547, 15897, 3415, 4617, 15623, 5806, 0]]
# 周一数据
# 取货 pick
p = [9, 9, 7, 8, 4, 8, 6, 9, 2, 2, 2, 2, 1, 2]
# 送货 deliver
q = [83, 95, 105, 106, 122, 100, 75, 87, 10, 3, 7, 6, 10, 11]

# 参数
K = 4  # 仓库车辆数
N = 15  # 节点数：s1~s8,med1~med6（仓库为1）
Med = 9  # 药店起始位点
Q = 360  # 车辆最大载货量
D = 60000  # 车辆距离上限
P = 0.003  # 单位距离空载运输成本（比例）
Pa = 0.001  # 单位距离最大载重运输成本（比例）
Pm = 0.2  # 药物货品包装成本（比例）
V = 6  # 车辆服务客户数量上限

# 调试参数
print_debug = 0  # 是否显示debug信息
init_population_num = 100  # 初始种群数量
evo_pairs = 50  # 每代多少个杂交对(新生成个体的数量 = evo_pairs*2)
swap_max = 80  # 最大单次交换次数
max_iterate = 1000  # 最大单次迭代步数
mutation_rate = 0.2  # 变异概率
mutation_num = 60  # 产生变异的个数


def item_generate():  # 生成个体
    w_max = -1
    s_max = -1
    nc = N - 1
    k_num_list = []  # 每辆车服务客户数量如 [4, 2, 3, 5]
    k_visit_arr = []  # 车辆服务客户顺序列表如 [[12, 11, 14, 3, 6, 13], [9, 4, 7, 2], [5, 8], [10, 15]]
    k_x_scatter = []  # 每辆车ij的列表如 [[[1,2],[2,3],...],[...],...]; [车[点[,]]]

    while w_max < 0 or s_max < 0 or s_max > D or w_max > Q:  # 要求生成的方案满足重量约束和距离约束

        # 生成每辆车要访问的顾客数
        while nc != 0:  # 如果不能完全分配要重新生成
            # 初始化生成
            k_num_list = []
            nc = N - 1
            # 生成
            for i in range(K - 1):
                num = random.randint(0, min(nc, V))
                nc -= num  # 从顾客中删除num个
                k_num_list.append(num)
            if nc < V:
                k_num_list.append(nc)
                nc = 0
        # print(k_num_list)
        k_num_list.sort(reverse=True)  # 从大到小排列车辆服务客户数量

        # 根据每辆车服务客户数量生成配送方案
        [k_visit_arr, k_x_scatter] = generate_d_arr(k_num_list)

        # 打印 for debug
        # print(k_visit_arr)
        # print(k_x_scatter)

        # 检测是否符合载货量要求（见函数）
        w_max = cal_w_max(k_visit_arr)
        # for debug
        if w_max > Q and print_debug:
            print("超重", w_max)

        # print("\n检测距离") # for debug
        # 检测是否符合最远距离要求
        s_max = cal_s_max(k_x_scatter)
        if s_max > D and print_debug:  # for debug
            print("超距离", s_max)

    # for debug
    # print("最终结果")
    # print(k_num_list)
    # print(k_visit_arr)
    # print(k_x_scatter)

    return [k_num_list, k_visit_arr, k_x_scatter]


# 输入车辆服务顺序矩阵，计算最大重量是否超标，返回最大重量
def cal_w_max(k_visit_arr):
    # print(k_visit_arr) # 打印输入序列
    # 检测是否符合载货量要求
    w_max = 0
    for karr in k_visit_arr:  # 每辆车
        q_all = []  # 初始化送货重量
        p_all = []  # 初始化取货重量
        # todo: 计算初始运货量的载重 w_sum
        for id in karr:  # 每个客户(id),从2开始（扫描数据）
            # print(id)
            q_all.append(q[id - 2])  # 加入指定客户的送货重量（q为向量）
            p_all.append(p[id - 2])  # 加入指定客户的取货重量
        w_sum = sum(q_all)  # 初始载重量（离开仓库时）
        w_max = max(w_sum, w_max)  # 更新最大值

        if w_max > Q:  # 如果此时已经超过最大允许载重量，直接跳出循环，不再计算
            break

        # for debug
        # print("q_all", q_all)
        # print("p_all",p_all)
        # print("w_sum",w_sum)

        # todo: 计算每一段路程的载重
        for i in range(len(karr)):  # 0~5 每个节点计算
            w_sum += (-q_all[i] + p_all[i])  # 更新过程重量
            w_max = max(w_sum, w_max)  # 更新最大值
            # for debug
            # print(w_sum) # 打印此运输过程的载重量
    # for debug
    # print(w_max) # 打印结果
    return w_max


def cal_s_max(k_x_scatter):  # 计算路程（最大值）
    s_max = 0
    for k in range(K):  # 每辆车都计算
        # print("车辆编号",k) # for debug
        s = []  # 初始化距离
        for o in k_x_scatter[k]:
            if (o != 0):
                # print(o,[o[0]-1,o[1]-1]) # for debug
                xi = o[0] - 1
                xj = o[1] - 1
                s.append(d[xi][xj])
        s_max = max(sum(s), s_max)

        if s_max > D:  # 如果已经超距离
            break
        # print("本轮计算距离和：",sum(s)) # for debug
    return s_max


# 根据每辆车的服务顺序生成配送方案
def generate_d_arr(k_num_list):  # 输入服务顺序，如 [4,2,3,5]
    # 生成客户列表
    customers = []
    for i in range(2, N + 1):  # (客户：2~15（14个）)
        # print(i)
        customers.append(i)
    # print(customers) # [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]

    # 生成每辆车服务的顺序
    #   和决策点
    k_visit_arr = []  # 车辆服务客户顺序列表如 [[12, 11, 14, 3, 6, 13], [9, 4, 7, 2], [5, 8], [10, 15]]
    k_x_scatter = []  # 每辆车ij的列表如 [[[1,2],[2,3],...],[...],...]; [车[点[,]]]
    for i in range(K):
        visit_arr = []  # 定义一辆车服务顺序向量
        x_scatter = []  # 访问点
        for j in range(k_num_list[i]):  # 根据服务数量生成每辆车要服务的客户的顺序
            # 抽取客户
            nc_remain = len(customers)
            c_rand = customers[random.randint(0, nc_remain - 1)]  # 随机选中的客户
            visit_arr.append(c_rand)
            customers.remove((c_rand))  # 从列表中删除客户

            # 组合决策点x
            if j == 0:  # 第一个
                x_scatter.append([1, c_rand])
            else:
                x_scatter.append([visit_arr[-2], visit_arr[-1]])  # 已经加进去了，所以[-2]，[-1]是最新的
            if j == (k_num_list[i] - 1):  # 如果是最后一个
                x_scatter.append([c_rand, 1])

        # 添加到列表
        k_visit_arr.append(visit_arr)  # 添加这辆车的访问客户顺序
        k_x_scatter.append(x_scatter)  # 添加这辆车的访问决策点

    return [k_visit_arr, k_x_scatter]


def get_visit_arr_by_gene(gene):
    structure = gene[:K]
    visit_arr = gene[K:]
    k_visit_arr = []  # 声明结果
    for num in structure:
        car_arr = []  # 一辆车要访问的客户
        for i in range(num):
            car_arr.append(visit_arr[i])
        visit_arr = visit_arr[num:]
        k_visit_arr.append(car_arr)
    return k_visit_arr


# print(get_visit_arr_by_gene([6, 6, 1, 1, 7, 15, 5, 11, 6, 13, 3, 14, 12, 10, 4, 9, 2, 8]))

def get_scatter(k_visit_arr):  # 获取决策变量点集
    # print(k_visit_arr) # for debug
    k_x_scatter = []  # 声明结果
    for arr in k_visit_arr:
        x_scatter = []  # 一辆车的访问点的集合
        for i in range(len(arr)):
            if i == 0:  # 第一个
                x_scatter.append([1, arr[i]])
            else:
                x_scatter.append([arr[i - 1], arr[i]])
            if i == (len(arr) - 1):  # 如果是最后一个
                x_scatter.append([arr[i], 1])
        k_x_scatter.append(x_scatter)
    return k_x_scatter


# print(get_scatter([[4, 12, 11, 15, 5, 7], [2, 9, 6], [10, 14, 3], [13, 8]]))

# 计算成本
def cal_score(k_visit_arr):
    score = 0.0
    p_w_sums = []  # 每段路径对应的取货量之和
    q_w_sums = []  # 每段路径运送的送货量之和
    w_sums = []  # 每段路径的总载重量
    for nodes in k_visit_arr:
        p_all = []
        q_all = []
        w_all = []

        for node in nodes:
            p_all.append(p[node - 2])  # 从向量中获取取货数值，刨除仓库占1，再考虑从0开始
            q_all.append(q[node - 2])  # 从向量中获取送货数值，同上
            # print("node",node) # for debug
        # for debug
        # print("nodes",nodes)
        # print(p_all)
        # print(q_all)
        p_w_sum = []
        q_w_sum = []
        for i in range(len(nodes)):  # 全路程取送货量计算（从仓库出发到回到仓库）
            p_w_sum.append(sum(p_all[:i + 1]))
            q_w_sum.append(sum(q_all[i:]))

        if len(q_w_sum) != 0:
            w_all.append(q_w_sum[0])  # 运往第一个节点
            for i in range(0, len(nodes) - 1):
                w_all.append(p_w_sum[i] + q_w_sum[i + 1])
            w_all.append(p_w_sum[-1])

        # for debug
        # print("p_w_sum",p_w_sum)
        # print("q_w_sum",q_w_sum)
        p_w_sums.append(p_w_sum)
        q_w_sums.append(q_w_sum)
        w_sums.append(w_all)

    # for debug
    # print("w_sums",w_sums)

    k_x_scatter = get_scatter(k_visit_arr)  # 获取散点集合
    for y in range(len(k_x_scatter)):
        for z in range(len(k_x_scatter[y])):
            # 转化为下标索引
            i = k_x_scatter[y][z][0] - 1
            j = k_x_scatter[y][z][1] - 1
            score += P * d[i][j]
            score += w_sums[y][z] * d[i][j] * Pa / Q
            # for debug
            # print(i+1,j+1,w_sums[y][z])
            # print(i+1,j+1,w_sums[y][z],w_sums[y][z]/Q)
    score += Pm * sum(q[Med - 1:])  # 配送药店药物额外加固费用
    # for debug
    # print(score)
    # print(q[Med-1:])
    # print(q)
    return score


# print(cal_score(get_visit_arr_by_gene([0,4,4,6,13,6,7,8,3,14,2,9,15,5,11,12,10,4])))

# [k_num_list, k_visit_arr, k_x_scatter] = item_generate()
# print("最终结果")
# print(k_num_list)
# print(k_visit_arr)
# print(k_x_scatter)


# [k_visit_arr,k_x_scatter] = generate_d_arr([4,2,3,5])
# score = cal_score([[4, 12, 11, 15, 5, 7], [2, 9, 6], [10, 14, 3], [13, 8]])
# print(score)

def get_gene(k_num_list, k_visit_arr):  # 获取基因(K+(N-1))；前K位为形状，后N-1位为顺序
    gene = copy.deepcopy(k_num_list)
    for items in k_visit_arr:
        for item in items:
            gene.append(item)
    return gene


# print(get_gene([5, 5, 2, 2],[[13, 9, 2, 6, 14], [15, 8, 12, 4, 11], [5, 7], [3, 10]]))

def grow(gene):  # 根据基因恢复
    structure = gene[:4]  # 切割位置在4位末尾
    content = gene[4:]
    adult = []  # 声明恢复目标
    for num in structure:
        arr = []  # 每辆车的服务顺序
        i = 0  # 声明切割点
        for i in range(num):
            arr.append(content[i])
        content = content[i + 1:]
        adult.append(arr)
    # for debug
    # print(structure,content)
    # print(gene)
    return [structure, adult]  # 返回结构和内容


# print(grow([5, 5, 2, 2, 13, 9, 2, 6, 14, 15, 8, 12, 4, 11, 5, 7, 3, 10]))


def init_gen():  # 初始种群
    population = []  # 声明初始种群

    for index in range(init_population_num):
        [k_num_list, k_visit_arr, k_x_scatter] = item_generate()
        # for debug
        # print(get_gene(k_num_list,k_visit_arr))
        # print(k_visit_arr)
        score = cal_score(k_visit_arr)
        gene = get_gene(k_num_list, k_visit_arr)
        population.append([score, gene])
    population.sort()  # 此处排序为分数从小到大

    print("已生成初始种群并完成排序")
    return population  # 返回种群：[[分数,基因],...]


def cross(item1, item2):  # 交叉
    structures = [item1[:4], item2[:4]]  # 储存结构
    gene_1 = item1[4:]
    gene_2 = item2[4:]
    # print(structures,gene_1,gene_2) # for debug

    swap_len = random.randint(1, int(len(gene_1) / 2))  # 交换长度
    sec_p = random.randint(0, len(gene_1) - swap_len)  # 截取位点
    insert_p = random.randint(0, len(gene_1))  # 插入位点
    # print(swap_len,sec_p,insert_p) # for debug

    sections = [gene_1[sec_p:sec_p + swap_len], gene_2[sec_p:sec_p + swap_len]]  # 截取的交换片段

    genes_s = [gene_1[:], gene_2[:]]  # 要返回的基因

    # print("insert_p",insert_p) # for debug
    for i in range(2):
        genes_s[i].insert(insert_p, 0)  # 插入的0无意义，只是一个标记
        # for debug
        # print("gene",i+1,genes_s[i])
        # print("index",genes_s[i].index(0))

        for sec in sections[i]:
            genes_s[i].remove(sec)
        tag = genes_s[i].index(0)  # 0的标记位点

        # for debug
        # print("tag",tag)
        # print("插入前",genes_s[i])
        # print("片段",sections[i])
        for j in range(swap_len):
            genes_s[i].insert(tag + j, sections[i][j])
        genes_s[i].remove(0)  # 移除标记位点
        # print("插入后",genes_s[i]) # for debug

    for i in range(K):
        genes_s[0].insert(i, structures[0][i])
        genes_s[1].insert(i, structures[1][i])
    return genes_s


# print(cross([6, 6, 1, 1, 7, 15, 5, 11, 6, 13, 3, 14, 12, 10, 4, 9, 2, 8],[6, 4, 3, 1, 13, 14, 11, 5, 3, 15, 6, 7, 8, 12, 4, 9, 2, 10]))

def evolution(population):

    if random.random() < mutation_rate:  # 触发变异
        print("触发变异")
        for i in range(mutation_num):
            [k_num_list, k_visit_arr, _] = item_generate()
            gene = get_gene(k_num_list, k_visit_arr)
            score = cal_score(k_visit_arr)
            population.append([score, gene])

    # 统计分数
    scores = []
    for item in population:
        # print(item) # for debug
        scores.append(item[0])
    # print(population) # for debug
    min_score = min(scores)  # 最低成本统计
    print("最低成本", min_score)

    # 计算比例
    proportion = []  # 比例（累计）
    proportion_sum = 0
    score_max = max(scores)  # 得到成本最高值
    adjusted_scores = []

    for score in scores:  # 预处理
        adjusted_scores.append((score_max - score + 20))

    scores_sum = sum(adjusted_scores)
    for score in adjusted_scores:
        proportion_sum += score / scores_sum
        proportion.append(proportion_sum)
    # for debug
    # print(proportion) # for debug 打印种群选择比例

    # for debug 测试选取
    selected_population = []  # 随机抽取的个体
    bests_selected = []  # 用于交叉的好的个体（不是了， 也改成了随机个体）
    pairs = evo_pairs  # 新增对数
    for i in range(pairs):  # 根据需要添加的个体数，抽取交换的一对
        r = random.random()
        for j in range(len(proportion)):
            if r < proportion[j]:
                selected_population.append(population[j][1])  # 添加随机抽取的个体基因
                break
        # bests_selected.append(population[-i][1])
        for j in range(len(proportion)):
            if r < proportion[j]:
                bests_selected.append(population[j][1])  # 添加随机抽取的个体基因
                break

    # for debug
    # print("selected_population",selected_population)
    # print("bests_selected",bests_selected)
    # print(population)
    # print(len(selected_population),"*",len(selected_population[0]))
    # print(len(bests_selected),"*",len(bests_selected[0]))

    for i in range(len(bests_selected)):  # 交叉后结果
        passed_gene = []
        count = 0
        while len(passed_gene) < 2 and count < swap_max:  # 合格的基因个数不够，且在交叉尝试的范围内

            genes = cross(bests_selected[i], selected_population[i])
            # for debug
            # print("bests_selected[", i, "]", bests_selected[i])
            # print("genes", genes)

            # 获取基本信息
            k_visit_arrs = [get_visit_arr_by_gene(genes[0]), get_visit_arr_by_gene(genes[1])]

            # print("k_visit_arrs",k_visit_arrs) # for debug
            k_x_scatters = [get_scatter(k_visit_arrs[0]), get_scatter(k_visit_arrs[1])]
            # 检验是否可行
            w_maxs = [cal_w_max(k_visit_arrs[0]), cal_w_max(k_visit_arrs[1])]
            s_maxs = [cal_s_max(k_x_scatters[0]), cal_s_max(k_x_scatters[1])]

            for j in range(2):
                if w_maxs[j] <= Q and s_maxs[j] <= D:  # 符合要求
                    passed_gene.append(genes[j])  # 添加到合格的基因

        if len(passed_gene) < 2:  # 没交叉出来
            gene_remain = 2 - len(passed_gene)  # 剩余多少个达到标准
            for r in range(gene_remain):
                [k_num_list, k_visit_arr, _] = item_generate()
                passed_gene.append(get_gene(k_num_list, k_visit_arr))

        # print("passed_gene",passed_gene) # for debug
        scores = [cal_score(get_visit_arr_by_gene(passed_gene[0])),
                  cal_score(get_visit_arr_by_gene(passed_gene[0]))]  # 只取前两个
        population.append([scores[0], passed_gene[0]])
        population.append([scores[1], passed_gene[1]])

    # population.sort() # 此处排序为分数从小到大
    # population = population[remove_num-1:]

    # for debug
    scores = []
    for item in population:
        # print(item) # for debug
        scores.append(item[0])
    # print(population) # for debug
    min_score = min(scores)  # 最高分统计
    print("进化后最低成本", min_score)

    population.sort()  # 排序
    # print("删除前",population)
    population = population[:init_population_num]  # 将数量调整回初始种群数量
    # for debug
    # print("种群大小",len(population))
    # print("删除后",population)
    return [min_score, population]


# evolution(init_gen())

def main():
    time_start = time.time()  # 记录开始时间
    gen1 = init_gen()
    stop_steps = 0
    cost = 999
    population = gen1[:]
    while stop_steps < max_iterate:
        print("迭代", stop_steps)
        [evo_cost, population] = evolution(population)
        if evo_cost < cost:  # 有进步
            stop_steps = 0  # 删除停止步数
            cost = min(evo_cost, cost)
        else:
            stop_steps += 1
    time_end = time.time()  # 记录结束时间
    print("最佳方案基因", population[0][1], "成本", population[0][0])
    print("最佳方案运输调配", get_visit_arr_by_gene(population[0][1]))
    print("运行时间", time_end - time_start, 's')


## 主函数及测试区
main()
