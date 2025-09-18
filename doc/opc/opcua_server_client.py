from opcua import Client, ua
from opcua.common.type_dictionary_buider import get_ua_class

# Configure and connect the client
client = Client("opc.tcp://127.0.0.1:55480") # 4840 is the default OPC UA port
client.connect()

root = client.get_root_node()
for i in root.get_child(["0:Objects","2:MyObject"]).get_children():
    print( i.get_browse_name() )
#for
val = root.get_child([ "0:Objects", "2:MyObject","2:MyVariable" ]).get_value()
print(val)
