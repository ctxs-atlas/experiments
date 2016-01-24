
address_bind_schema = {
      "type" : "address_bind",
      "attributes" : [
	      {
		   "name" : "ipaddress",
		   "type" : "ipaddress",
                   "description" : "IP address on which the listener listens for incoming requests",
		   "required" : False,
		   "updatable" : True
	      },      
	      {
		   "name" : "port",
		   "type" : "tcp-port",
                   "description" : "port number on which the listener listens for incoming requests",
		   "required" : True,
		   "updatable" : True
	      }
       ]
}


schema_types = {
                 "address_bind" : address_bind_schema
               }



