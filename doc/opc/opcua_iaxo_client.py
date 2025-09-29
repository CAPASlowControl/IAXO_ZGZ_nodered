from opcua import Client, ua
from opcua.common.type_dictionary_buider import get_ua_class

# Configure and connect the client
client = Client("opc.tcp://127.0.0.1:55480/") # 4840 is the default OPC UA port
client.connect()

# Browse the server
root = client.get_root_node()
llist = root.get_child("0:Objects").get_child("1:IAXO-ZGZ").get_children()
for e in llist:
    print("ITEM:", e.get_browse_name())
    try:
        print(e.get_value() )
    except:
        pass
    for m in e.get_children():
        print("---SUBITEM", m.get_browse_name())
        try:
            print(m.get_value() )
        except:
            pass
        for k in m.get_children():
            print("------SUBSUB-ITEM", k.get_browse_name())
            print(k.get_browse_name())
            try:
                print(k.get_value() )
            except:
                pass

        #for
                #if (isinstance(NodeClass.Variable, m.get_node_class())):
                #    print(m.get_value())
    #for

zgz = root.get_child("0:Objects").get_child("1:IAXO-ZGZ")
gas  = zgz.get_child("1:GAS").get_child("1:Pressure")
for i in gas.get_children():
   print(i.get_browse_name())
#for

Pinlet = gas.get_child("1:Pinlet")

print("From Parent")
print(Pinlet.get_value() )


print("Using full browse path")

Pinlet = root.get_child([ "0:Objects","1:IAXO-ZGZ","1:GAS","1:Pressure","1:Pinlet" ]).get_value()
print(Pinlet)

node_id = "ns=1;s=Pinlet"
node = client.get_node(node_id)
Pinlet = node.get_value()

print("Using node_id")
print(Pinlet)

client.disconnect()
