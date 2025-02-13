import csv
import os
import time
import sys
maxInt = sys.maxsize


def write_to_csv(file_name, data):

    with open(file_name, 'a', newline='\n',encoding='utf-8') as csvfile:
        csv_writer = csv.writer(csvfile,doublequote=False,
                                delimiter='\x01',
                                escapechar=',')
                        # escapechar=',',
                        # quotechar='"',
                        # quoting=csv.QUOTE_ALL)
        two_d_array = [element.split(',') for element in data]
        csv_writer.writerows(two_d_array)

def create_directory_and_file(directory, filename,header):
    try:
        file_path = os.path.join(directory, filename)
        delete_file(file_path)
        os.makedirs(directory, exist_ok=True)

        file_path = os.path.join(directory, filename)
        with open(file_path, 'w', encoding='utf-8',newline='\n') as csvfile:
            csv_writer = csv.writer(csvfile,doublequote=False, delimiter='\x01')
                        # escapechar=',',
                        # quotechar='"',
                        # quoting=csv.QUOTE_ALL)
            csv_writer.writerow(header)
        print(f"Directory '{directory}' and file '{filename}' have been created.")
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False

def delete_file(file_path):

    if os.path.exists(file_path):
        os.remove(file_path)
        print(f"File '{file_path}' has been deleted.")




if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("缺少参数")
        sys.exit(1)

    while True:
        # decrease the maxInt value by factor 10
        # as long as the OverflowError occurs.

        try:
            csv.field_size_limit(maxInt)
            break
        except OverflowError:
            maxInt = int(maxInt / 10)

    g_node_header = ["id","name"]
    c_node_header = ["id", "name", "level","role"]
    edge_header = ["src_id","dst_id","sharehold","group_id"]
    company_csv_name = "Company.csv"
    group_csv_name = "GROUP.csv"
    g_t_c_csv_name = "GROUP_relation_Company.csv"
    c_t_c_csv_name = "Company_relation_Company.csv"
    csv_path = sys.argv[2]
    source_data_file = sys.argv[1]
    size = 1000000




    if not os.path.exists(source_data_file) :
        print(f"File '{source_data_file}' not exists.")
        sys.exit(1)
    #创建输出文件以及表头
    start_time = time.time()


    create_directory_and_file(csv_path, company_csv_name, c_node_header)
    create_directory_and_file(csv_path, group_csv_name, g_node_header)
    create_directory_and_file(csv_path, g_t_c_csv_name, edge_header)
    create_directory_and_file(csv_path, c_t_c_csv_name, edge_header)


    with open(source_data_file, 'r', newline='', encoding='utf-8') as tsvfile:

        csv_reader = csv.reader(tsvfile, delimiter='\x01',escapechar='', quotechar='"', strict=True)
        next(csv_reader)
        group_ids = []
        stmt_list = []
        # group_nodes = []
        # company_nodes = []
        # relation1_edges = []
        # relation2_edges = []
        # node_set = set()
        # group_set = set()
        # edge_set = set()
        cnt = 0;
        for row in csv_reader:
            print(row)
            tmp_c = row[0]
            print(tmp_c)
            stmt = "match (n:GROUP {id : '" + tmp_c + "'}) return n limit 10;"
            print(stmt)
            stmt_list.append(stmt)
            group_ids.append(tmp_c)
        
        print(group_ids)
        print(stmt_list)
        with open('out.sql', 'w', newline='', encoding='utf-8') as outfile:
            #outfile.write("".join(stmt_list))
            for string in stmt_list:
                outfile.write(string + "\n")
        #     try:
        #         #print(row)
        #         path = row[-1].replace('\\', '').replace('[','').replace(']','')
        #             # .replace('"', '').replace('\\', '').replace('[','').replace(']','')
        #         # print(path)
        #         tmp_c = row[2] + "," + row[3]+","+row[5] + "," + row[4]
        #         company_nodes.append(tmp_c.strip())

        #         # if tmp_c not in node_set:
        #         #     company_nodes.append(tmp_c.strip() + "," + row[5])
        #         #     node_set.add(tmp_c.strip())
        #         if len(path) < 6 and row[5] == '0':
        #             #['ICN5040822716', '烟台新华国际旅行社有限公司', 'ICN5040822716', '烟台新华国际旅行社有限公司', '01', '0', '', '', '', '[]']
        #             tmp_g = row[0]+","+row[1]
        #             # tmp_c = row[2] + "," + row[3]+","+row[5] + "," + row[4]
        #             tmp_r = row[0]+","+row[2]+","+''+","+row[0]
        #             # company_nodes.append(tmp_c.strip())
        #             if tmp_g not in group_set:
        #                 group_nodes.append(tmp_g.strip())
        #                 group_set.add(tmp_g.strip())
        #             # if tmp_c not in node_set:
        #             #     company_nodes.append(tmp_c.strip()+","+row[5])
        #             #     node_set.add(tmp_c.strip())
        #             if tmp_r not in edge_set:
        #                 relation1_edges.append(tmp_r.strip())
        #                 edge_set.add(tmp_r.strip())
        #         else:
        #             for p in path.split(",") :

        #                 split_data = p.split("->")
        #                 raw_nodes = []
        #                 raw_edges = []
        #                 # print(path)
        #                 for item in split_data:

        #                     raw_data = item.split(":")
        #                     if len(raw_data) == 2 and len(raw_data[0].split(".")) == 2:
        #         # if len(raw_data) == 2 :
        #                         edge,node = raw_data
        #                     # if node not in node_set:
        #                         raw_nodes.append(node)
        #                         # node_set.add(node)
        #                     # if edge not in edge_set :
        #                         raw_edges.append(edge)
        #                         #edge_set.add(edge)
        #                     else:
        #                         raw_nodes.append(item)



        #                 for i, edge in enumerate(raw_edges):
        #                     src = [item.strip().strip('"') for item in raw_nodes[i].split('|')]
        #                     dst = [item.strip().strip('"') for item in raw_nodes[i+1].split('|')]
        #                     data = src[0]+","+dst[0]+","+"{:.2%}".format(float(edge))+","+row[0]

        #                     # data = raw_nodes[i].split("|")[0] + "," + raw_nodes[i + 1].split("|")[0] + "," + "{:.2%}".format(float(edge)) + "," + row[0]

        #                     if data.strip() not in edge_set :
        #                         relation2_edges.append(data.strip())
        #                         edge_set.add(data.strip())

        #                 # for i, node in enumerate(raw_nodes):
        #                 #     if i != len(raw_nodes) -1:
        #                 #         data = raw_nodes[i].replace("|", ",").strip()
        #                 #         if data not in node_set:
        #                 #             company_nodes.append(data+","+'')
        #                 #             node_set.add(data)
        #         cnt = cnt + 1

        #         if cnt % size == 0 :
        #             write_to_csv( os.path.join(csv_path, company_csv_name),company_nodes)
        #             company_nodes.clear()
        #             write_to_csv(os.path.join(csv_path, group_csv_name), group_nodes)
        #             group_nodes.clear()
        #             write_to_csv(os.path.join(csv_path, g_t_c_csv_name), relation1_edges)
        #             relation1_edges.clear()
        #             write_to_csv(os.path.join(csv_path, c_t_c_csv_name), relation2_edges)
        #             relation2_edges.clear()
        #             node_set.clear()
        #             edge_set.clear()
        #             group_set.clear()
        #             print(f"已处理[ '{cnt}' ]条,耗时[ '{time.time() - start_time}' ] 秒")
        #     except IndexError:
        #         print("Error: Index error occurred while processing data.")
        #     except ValueError as e:
        #         print(f"Error: {e}. Unable to convert edge value to float.")

        # write_to_csv(os.path.join(csv_path, company_csv_name), company_nodes)
        # company_nodes.clear()
        # write_to_csv(os.path.join(csv_path, group_csv_name), group_nodes)
        # group_nodes.clear()
        # write_to_csv(os.path.join(csv_path, g_t_c_csv_name), relation1_edges)
        # relation1_edges.clear()
        # write_to_csv(os.path.join(csv_path, c_t_c_csv_name), relation2_edges)
        # relation2_edges.clear()
        # print(f"完成已处理[ '{cnt}' ]条,耗时[ '{time.time() - start_time}' ] 秒")


    # if os.path.exists('aaaa.csv'):
    #     os.remove('aaaa.csv')
    #
    # write_to_csv('aaaa.csv',node_header,None,False)
    # write_to_csv('aaaa.csv', None, company_nodes, True)
    # print(company_nodes)








