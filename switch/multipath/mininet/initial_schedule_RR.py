
import subprocess
import random

if __name__ == "__main__":
    service_1 = [1, 1, 1]
    order_1 = [1,2,3]
    s175='9090'
    s181='9092'
    s183='9093'
    s185='9094'
    s187='9095'
    s177='9091'
    eccn = '0'
    multipath = '1'


    ## switch s175
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s175, 
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

    ## switch s181
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s181, 
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

    ## switch s183
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s183, 
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

    ## switch s185
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s185, 
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

    ## switch s187
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s187, 
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

    ## switch s177
    psi = subprocess.Popen('simple_switch_CLI --thrift-port '+ s177, 
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



    print('read register on s175')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s175, 
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

    print('read register on s181')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s181, 
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

    print('read register on s183')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s183, 
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

    print('read register on s185')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s185, 
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

    print('read register on s187')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s187, 
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

    print('read register on s177')
    p = subprocess.Popen('simple_switch_CLI --thrift-port '+ s177, 
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

    
    