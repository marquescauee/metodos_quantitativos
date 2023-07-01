for i in range(1, 30):
    original_instance = open('./'+str(i)+'/inst'+str(i)+'.txt', 'r')
    formated_instance = open('./'+str(i)+'/result'+str(i)+'.txt', 'w')

    for line in original_instance:
        formated_instance.writelines(line.strip()[7] + line.strip()[8] + line.strip()[9] + line.strip()[10] + " " + line.strip()[17] + line.strip()[18] + line.strip()[19] + line.strip()[20] + "\n")

    print(f"instancia {i} concluida com sucesso")

    formated_instance.close()
    original_instance.close()


