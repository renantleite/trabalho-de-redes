from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel
import time

def criar_rede_pox():
    print("*** Criando Topologia RNP para Controlador POX")

    # Definimos que o controlador será remoto (O POX rodando na outra janela)
    net = Mininet(
        controller=RemoteController,
        switch=OVSSwitch,
        link=TCLink,
        autoSetMacs=True
    )
    
    # Adicionando o Controlador (IP local, porta padrão 6633)
    print("*** Conectando ao Controlador POX...")
    c0 = net.addController('c0', controller=RemoteController, ip='127.0.0.1', port=6633)

    print("*** Criando Switches (PoPs Estaduais)")
    # NOTA: Removemos 'protocols=OpenFlow13' para compatibilidade com POX
    # failMode='secure': Se o POX cair, o switch trava (segurança SDN)
    s_df = net.addSwitch('s_df', dpid='1', failMode='secure')
    s_sp = net.addSwitch('s_sp', dpid='2', failMode='secure')
    s_rj = net.addSwitch('s_rj', dpid='3', failMode='secure')
    s_ce = net.addSwitch('s_ce', dpid='4', failMode='secure')
    s_pe = net.addSwitch('s_pe', dpid='5', failMode='secure')
    s_rs = net.addSwitch('s_rs', dpid='6', failMode='secure')
    s_am = net.addSwitch('s_am', dpid='7', failMode='secure')

    print("*** Criando Hosts")
    def add_host_to_switch(switch_obj, name):
        h = net.addHost(name)
        net.addLink(h, switch_obj, bw=100, delay='1ms')
        return h

    add_host_to_switch(s_df, 'h_df')
    add_host_to_switch(s_sp, 'h_sp')
    add_host_to_switch(s_rj, 'h_rj')
    add_host_to_switch(s_ce, 'h_ce')
    add_host_to_switch(s_pe, 'h_pe')
    add_host_to_switch(s_rs, 'h_rs')
    add_host_to_switch(s_am, 'h_am')

    print("*** Criando Links Backbone (RNP)")
    net.addLink(s_df, s_sp, bw=100, delay='10ms')
    net.addLink(s_df, s_rj, bw=100, delay='12ms')
    net.addLink(s_sp, s_rj, bw=100, delay='5ms')
    net.addLink(s_sp, s_rs, bw=80, delay='15ms')
    net.addLink(s_df, s_ce, bw=80, delay='25ms')
    net.addLink(s_ce, s_pe, bw=80, delay='10ms')
    net.addLink(s_pe, s_rj, bw=80, delay='20ms')
    net.addLink(s_df, s_am, bw=50, delay='45ms')
    net.addLink(s_ce, s_am, bw=50, delay='40ms')

    print("*** Iniciando a rede")
    net.start()

    # Não precisamos configurar STP manual aqui. 
    # O módulo 'openflow.spanning_tree' do POX vai fazer isso sozinho.

    print("*** Aguardando 15s para o POX descobrir a topologia...")
    time.sleep(15)

    print("*** Iniciando CLI (Tente 'pingall' para ver o POX trabalhar)")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    criar_rede_pox()