# 1. Instalar Mininet e o Switch OpenvSwitch
sudo apt install mininet openvswitch-switch -y

# 2. Testar se instalou corretamente (deve rodar um teste rápido)
sudo mn --test pingall
Se aparecer "Results: 0% dropped", o Mininet está pronto



# 1. Voltar para a pasta raiz
cd ~

# 2. Clonar o repositório oficial do POX
git clone https://github.com/noxrepo/pox

# 3. (Opcional) Mudar para a versão experimental (melhor suporte a Python 3)
cd pox
git checkout gar-experimental
cd ..


cd ~/pox
python3 pox.py forwarding.l2_learning openflow.discovery openflow.spanning_tree --no-flood --hold-down

Aguarde aparecer a mensagem: POX ... is up.

# Rode o script com permissões de superusuário
sudo python3 projeto_final.py

#caso de erro limpe o mn
sudo mn -c

Testar Conectividade: Dentro da CLI do Mininet (mininet>), use:

pingall (Testa todos contra todos)

h_df ping h_sp (Teste individual)
