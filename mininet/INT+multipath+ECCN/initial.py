
import subprocess
import random

if __name__ == "__main__":
    service_1 = [1, 1, 1]
    order_1 = [1,2,3]
    s176='9090'
    s178='9091'
    s182='9092'
    s184='9093'
    s186='9094'
    s188='9095'
    eccn = '0'
    multipath = '0'


    ## switch s176
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s176, 
                            shell=True,stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    psi.stdin.write('register_reset transmition_model\n')
    psi.stdin.write('register_write transmition_model 0 ' + eccn + '\n')
    psi.stdin.write('register_write transmition_model 1 ' + multipath + '\n')
    psi.stdin.write('register_reset multipath_ability\n')
    psi.stdin.write('register_write multipath_ability 0 0\n')
    psi.stdin.write('register_reset multipath_initial\n')
    psi.stdin.write('register_reset multipath_count\n')
    out,err = psi.communicate()
    print(err)

    ## switch s182
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s182, 
                            shell=True,stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    psi.stdin.write('register_reset transmition_model\n')
    psi.stdin.write('register_write transmition_model 0 ' + eccn + '\n')
    psi.stdin.write('register_write transmition_model 1 ' + multipath + '\n')
    psi.stdin.write('register_reset multipath_ability\n')
    psi.stdin.write('register_write multipath_ability 0 1\n')
    psi.stdin.write('register_reset multipath_initial\n')
    psi.stdin.write('register_write multipath_initial 2 ' + str(service_1[0]) + '\n')
    psi.stdin.write('register_write multipath_initial 3 ' + str(service_1[1]) + '\n')
    psi.stdin.write('register_write multipath_initial 4 ' + str(service_1[2]) + '\n')
    psi.stdin.write('register_reset multipath_count\n')
    psi.stdin.write('register_write multipath_count 2 ' + str(service_1[0]) + '\n')
    psi.stdin.write('register_write multipath_count 3 ' + str(service_1[1]) + '\n')
    psi.stdin.write('register_write multipath_count 4 ' + str(service_1[2]) + '\n')
    psi.stdin.write('register_reset multipath_order\n')
    psi.stdin.write('register_write multipath_order 2 ' + str(order_1[0]) + '\n')
    psi.stdin.write('register_write multipath_order 3 ' + str(order_1[1]) + '\n')
    psi.stdin.write('register_write multipath_order 4 ' + str(order_1[2]) + '\n')
    out,err = psi.communicate()
    print(err)

    ## switch s184
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s184, 
                            shell=True,stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    psi.stdin.write('register_reset transmition_model\n')
    psi.stdin.write('register_write transmition_model 0 ' + eccn + '\n')
    psi.stdin.write('register_write transmition_model 1 ' + multipath + '\n')
    psi.stdin.write('register_reset multipath_ability\n')
    psi.stdin.write('register_write multipath_ability 0 0\n')
    psi.stdin.write('register_reset multipath_initial\n')
    psi.stdin.write('register_reset multipath_count\n')
    out,err = psi.communicate()
    print(err)

    ## switch s186
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s186, 
                            shell=True,stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    psi.stdin.write('register_reset transmition_model\n')
    psi.stdin.write('register_write transmition_model 0 ' + eccn + '\n')
    psi.stdin.write('register_write transmition_model 1 ' + multipath + '\n')
    psi.stdin.write('register_reset multipath_ability\n')
    psi.stdin.write('register_write multipath_ability 0 0\n')
    psi.stdin.write('register_reset multipath_initial\n')
    psi.stdin.write('register_reset multipath_count\n')
    out,err = psi.communicate()
    print(err)

    ## switch s188
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s188, 
                            shell=True,stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    psi.stdin.write('register_reset transmition_model\n')
    psi.stdin.write('register_write transmition_model 0 ' + eccn + '\n')
    psi.stdin.write('register_write transmition_model 1 ' + multipath + '\n')
    psi.stdin.write('register_reset multipath_ability\n')
    psi.stdin.write('register_write multipath_ability 0 1\n')
    psi.stdin.write('register_reset multipath_initial\n')
    psi.stdin.write('register_write multipath_initial 2 ' + str(service_1[0]) + '\n')
    psi.stdin.write('register_write multipath_initial 3 ' + str(service_1[1]) + '\n')
    psi.stdin.write('register_write multipath_initial 4 ' + str(service_1[2]) + '\n')
    psi.stdin.write('register_reset multipath_count\n')
    psi.stdin.write('register_write multipath_count 2 ' + str(service_1[0]) + '\n')
    psi.stdin.write('register_write multipath_count 3 ' + str(service_1[1]) + '\n')
    psi.stdin.write('register_write multipath_count 4 ' + str(service_1[2]) + '\n')
    psi.stdin.write('register_reset multipath_order\n')
    psi.stdin.write('register_write multipath_order 2 ' + str(order_1[0]) + '\n')
    psi.stdin.write('register_write multipath_order 3 ' + str(order_1[1]) + '\n')
    psi.stdin.write('register_write multipath_order 4 ' + str(order_1[2]) + '\n')
    out,err = psi.communicate()
    print(err)

    ## switch s178
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s178, 
                            shell=True,stdin=subprocess.PIPE, 
                            stdout=subprocess.PIPE, 
                            stderr=subprocess.PIPE, 
                            universal_newlines=True)
    psi.stdin.write('register_reset transmition_model\n')
    psi.stdin.write('register_write transmition_model 0 ' + eccn + '\n')
    psi.stdin.write('register_write transmition_model 1 ' + multipath + '\n')
    psi.stdin.write('register_reset multipath_ability\n')
    psi.stdin.write('register_write multipath_ability 0 0\n')
    psi.stdin.write('register_reset multipath_initial\n')
    psi.stdin.write('register_reset multipath_count\n')
    out,err = psi.communicate()
    print(err)



    print('read register on s176')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s176, 
                        shell=True,stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        universal_newlines=True) 
    p.stdin.write('register_read transmition_model\n')
    p.stdin.write('register_read multipath_ability\n')
    p.stdin.write('register_read multipath_initial\n')
    p.stdin.write('register_read multipath_count\n')
    p.stdin.write('register_read multipath_order\n')
    out,err = p.communicate()
    print(out)

    print('read register on s182')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s182, 
                        shell=True,stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        universal_newlines=True) 
    p.stdin.write('register_read transmition_model\n')
    p.stdin.write('register_read multipath_ability\n')
    p.stdin.write('register_read multipath_initial\n')
    p.stdin.write('register_read multipath_count\n')
    p.stdin.write('register_read multipath_order\n')
    out,err = p.communicate()
    print(out)

    print('read register on s184')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s184, 
                        shell=True,stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        universal_newlines=True) 
    p.stdin.write('register_read transmition_model\n')
    p.stdin.write('register_read multipath_ability\n')
    p.stdin.write('register_read multipath_initial\n')
    p.stdin.write('register_read multipath_count\n')
    p.stdin.write('register_read multipath_order\n')
    out,err = p.communicate()
    print(out)

    print('read register on s186')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s186, 
                        shell=True,stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        universal_newlines=True) 
    p.stdin.write('register_read transmition_model\n')
    p.stdin.write('register_read multipath_ability\n')
    p.stdin.write('register_read multipath_initial\n')
    p.stdin.write('register_read multipath_count\n')
    p.stdin.write('register_read multipath_order\n')
    out,err = p.communicate()
    print(out)

    print('read register on s188')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s188, 
                        shell=True,stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        universal_newlines=True) 
    p.stdin.write('register_read transmition_model\n')
    p.stdin.write('register_read multipath_ability\n')
    p.stdin.write('register_read multipath_initial\n')
    p.stdin.write('register_read multipath_count\n')
    p.stdin.write('register_read multipath_order\n')
    out,err = p.communicate()
    print(out)

    print('read register on s178')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s178, 
                        shell=True,stdin=subprocess.PIPE, 
                        stdout=subprocess.PIPE, 
                        stderr=subprocess.PIPE, 
                        universal_newlines=True) 
    p.stdin.write('register_read transmition_model\n')
    p.stdin.write('register_read multipath_ability\n')
    p.stdin.write('register_read multipath_initial\n')
    p.stdin.write('register_read multipath_count\n')
    p.stdin.write('register_read multipath_order\n')
    out,err = p.communicate()
    print(out)

    
    