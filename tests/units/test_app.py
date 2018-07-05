

from unittest import TestCase
import tempfile

import app

import sys,os

class ConsoleAppTest(TestCase):

    def setUp(self):
        # crear arixu amb nums del 1 al 100
        self.tmpfile = open("tmp_nums.txt","w")
        self.errfile = open("err_nums.txt","w")
        self.errfile.write( "introduim string de test\n" )
        for i in range(101):
            self.tmpfile.write( str(i)+"\n" )
            self.errfile.write( str(i)+"\n" )
        self.tmpfile.close()

        # redirigim stdout per no liarla (monkey patch)
        self.sys_stdout = sys.stdout
        self.outfile = open("outfile.txt","w")
        sys.stdout = self.outfile

    def tearDown(self):
        # esborrem arxiu de numeros per inputs
        os.unlink( self.tmpfile.name )
        #os.unlink( self.errfile.name )
        # retornem stdout sl sistema
        sys.stdout = self.sys_stdout
        # esborrem arxiu de sortida stdout
        self.outfile.close()

    def test_zexisteix_funcio_endevina(self):
        self.assertTrue( hasattr(app, "endevina"), "La app ha de tenir una funció endevina()" )
        self.assertTrue( callable(app.endevina), "L'objecte 'endevina' de la app no és una funció" )

    def test_endevina_unitari(self):
        # test unitari
        trobat = False
        # patchejem el stdin amb els numeros (monkey patch)
        # a l'arxiu hi ha els numeros del 1 al 100, ho resolem per "força bruta"
        stdin = sys.stdin
        sys.stdin = open( self.tmpfile.name , "r")
        try:
            # endevinem numero
            app.endevina()
            trobat = True
        except EOFError:
            # arribem al final del fitxer i no trobem el numero
            trobat = False
        # recuperem stdin
        sys.stdin.close()
        sys.stdin = stdin
        # assert
        self.assertTrue( trobat , msg="Numero no endevinable. Ha de ser del 1 al 100 i no pot canviar a cada volta." )

    def test_endevina_estadistic(self):
        # repetim el test molts cops per assegurar que no es fan randoms continus
        # en alguna de les 1000 iteracions hauria de fallar
        for j in range(1000):
            self.test_endevina_unitari()

    def test_proteccio_input(self):
        # test unitari
        trobat = False
        # patchejem el stdin amb els numeros (monkey patch)
        # a l'arxiu hi ha els numeros del 1 al 100, ho resolem per "força bruta"
        stdin = sys.stdin
        sys.stdin = open("err_nums.txt", "r")
        try:
            # endevinem numero
            app.endevina()
            trobat = True
        except ValueError:
            trobat = False
            raise Exception("La app falla quan entres text enlloc d'un numero")
        except EOFError:
            # arribem al final del fitxer i no trobem el numero
            trobat = False
        # recuperem stdin
        sys.stdin.close()
        sys.stdin = stdin
        # assert
        self.assertTrue(trobat, msg="Numero no endevinable. Ha de ser del 1 al 100 i no pot canviar a cada volta.")
