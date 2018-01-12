import tornado.ioloop
import tornado.web
import sqlite3
import json


class ErrorHandler(tornado.web.ErrorHandler, tornado.web.RequestHandler):
    def write_error(self, status, **kwargs):
        self.write(str(status)+" HTTP ERROR\n")



class ZespolHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()
        
    def write_json(self):
        output = json.dumps(self.response)
        self.write(output)
        
    def get(self,id):
        
        conn = sqlite3.connect("data/sqlite.db")
        c = conn.cursor()
        try:
            c.execute("select * from zespoly where id = ?",(id,))
            self.set_header('Content-Type', 'application/json')
            row = c.fetchone()
            if row is None:
                raise Exception()
            else:
        	    self.write(json.dumps({"id": row[0], "nazwa": row[1], "miasto": row[2], "punkty": row[3]},sort_keys=True, indent=4)+"\n")
        except:
            message = 'No team member'
            self.send_error(404, message=message)
        conn.commit()
        c.close()
        
    def delete(self, id):
        conn = sqlite3.connect("data/sqlite.db")
        c = conn.cursor()
        try:
            c.execute("SELECT * FROM zespoly where id = ?",(id,))
            item = c.fetchone()
            if item is None:
                raise Exception()
            c.execute("DELETE FROM zespoly WHERE id = ?", (id,))
            conn.commit()
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({"message":"OK"}))
        except:
            message = 'Cannot delete'
            self.send_error(400, message=message)
        c.close()
        
    def patch(self,id):
        conn = sqlite3.connect("data/sqlite.db")
        c = conn.cursor()
        c.execute("SELECT * FROM zespoly WHERE id = ?", (id,))
        row = c.fetchone()
        if row is None:
            message = 'No item with this id'
            self.send_error(400, message=message)
            return
        else:
            try:
            	json_data = json.loads(self.request.body)
            except:
            	message = 'Unable to parse JSON.'
                self.send_error(400, message=message)
            	return
            try:
            	nazwa = str(json_data["nazwa"])
            except:
            	nazwa = row[1]
            try:
            	miasto = str(json_data["miasto"])
            except:
            	miasto = row[2]
            try:
            	punkty = int(json_data["punkty"])
            except:
            	punkty = row[3]
            try:
            	c.execute("UPDATE zespoly SET nazwa=?, miasto=?, punkty=? WHERE id = ?", (nazwa,miasto,punkty,id))
            	self.write("OK");
            except:
            	message = "Couldn't patch record"
                self.send_error(500, message=message)
            conn.commit()
            c.close()
   


class ZespolyHandler(tornado.web.RequestHandler):
    def write_error(self, status_code, **kwargs):
        if 'message' not in kwargs:
            if status_code == 405:
                kwargs['message'] = 'Invalid HTTP method.'
            else:
                kwargs['message'] = 'Unknown error.'

        self.response = kwargs
        self.write_json()
        
    def write_json(self):
        output = json.dumps(self.response)
        self.write(output)
        
    def get(self):
        try:
			page = int(self.get_argument("page"))
        except:
			page = 1
        first = (page - 1)  * 10
        last = page * 10
        respone = []
        
        conn = sqlite3.connect("data/sqlite.db")
        c = conn.cursor()
        c.execute("SELECT * FROM zespoly")
        i = 0
        j=0
        for row in c:
        	if ((j >= first) and (j < last)) and (i<10):
        		respone.append({"id": row[0], "nazwa": row[1], "miasto": row[2], "punkty": row[3]})
        		i+=1
        	j+=1
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(respone, ensure_ascii=False,sort_keys=True, indent=4))
        conn.commit()
        c.close()

        
    def post(self):
        try:
            json_data = json.loads(self.request.body)
        except:
            message = 'Unable to parse JSON.'
            self.send_error(400, message=message)
            return
        try:
            nazwa = str(json_data["nazwa"])
        except:
            message = 'Unable to parse JSON.'
            self.send_error(400, message=message)
        try:
            miasto = str(json_data["miasto"])
        except:
            message = 'Unable to parse JSON.'
            self.send_error(400, message=message)
            return
        try:
            punkty = str(json_data["punkty"])
        except:
            punkty = 0
        conn = sqlite3.connect("data/sqlite.db")
        c = conn.cursor()
        try:
            c.execute("INSERT INTO zespoly VALUES(NULL,?,?,?)",(nazwa,miasto,punkty))
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({"id": c.lastrowid}))
            conn.commit()
        except:
            message = "Couldn't add record.\n"
            self.send_error(500, message=message)
        c.close()
                   
    def delete(self):
        conn = sqlite3.connect("data/sqlite.db")
        c = conn.cursor()
        try:
            c.execute("DELETE FROM zespoly")
            self.set_header('Content-Type', 'application/json')
            self.write(json.dumps({"message":"OK"}))
        except:
            message = 'Cannot delete'
            self.send_error(400, message=message)
        conn.commit()
        c.close()

    def patch(self):
        conn = sqlite3.connect("data/sqlite.db")
        c = conn.cursor()
        try:
        	json_data = json.loads(self.request.body)
        except:
            message = 'Unable to parse JSON.'
            self.send_error(400, message=message)
            return
        for row in json_data:
            try:
            	nazwa = str(row["nazwa"])
            except:
                message="Unable to patch object \n"
                self.send_error(500, message=message)
            	continue
            try:
            	miasto = str(row["miasto"])
            except:
            	message="Unable to patch object \n"
            	self.send_error(500, message=message)
            	continue
            try:
            	punkty = int(row["punkty"])
            except:
            	punkty = 0
            try:
            	c.execute("UPDATE zespoly SET nazwa=?, miasto=?, punkty=? WHERE id = ?", (nazwa,miasto,punkty,row["id"]))
            	self.write("OK");
            except:
            	message = "Couldn't patch record"
                self.send_error(500, message=message)
        conn.commit()
        c.close()
        
if __name__ == "__main__":
	settings = {
		"autoreload": True,
		"debug": True,
		"default_handler_class": ErrorHandler,
		"default_handler_args": dict(status_code=404)
	}
	application = tornado.web.Application([
		("/teams/?", ZespolyHandler),
		("/teams/([0-9]+)", ZespolHandler)
	], **settings)
	application.listen(8080)
	tornado.ioloop.IOLoop.instance().start()