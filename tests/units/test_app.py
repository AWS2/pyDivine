

from unittest import TestCase
import sys,os

import app

# flag per guardar sortida en un arxiu
# (i evitar omplir la consola amb missatges)
SAVE_STDOUT = True


class ConsoleAppTest(TestCase):

    @classmethod
    def setUpClass(cls):
        # crear arixu amb nums del 1 al 100
        cls.tmpfile = open("tmp_nums.txt","w")
        cls.errfile = open("err_nums.txt","w")
        cls.errfile.write( "introduim string de test\n" )
        for i in range(101):
            cls.tmpfile.write( str(i)+"\n" )
            cls.errfile.write( str(i)+"\n" )
        cls.tmpfile.close()

        # redirigim stdout per no liarla (monkey patch)
        cls.sys_stdout = sys.stdout
        cls.outfile = open("outfile.txt","w")
        cls.stdout = cls.outfile

    @classmethod
    def tearDownClass(cls):
        # esborrem arxiu de numeros per inputs
        os.unlink( cls.tmpfile.name )
        os.unlink( cls.errfile.name )
        # retornem stdout al sistema
        cls.stdout = cls.sys_stdout
        # tanquem i esborrem arxiu de sortida stdout
        cls.outfile.close()
        os.unlink( cls.outfile.name )

    def test_zexisteix_funcio_endevina(self):
        self.assertTrue( hasattr(app, "endevina"), "La app ha de tenir una funció endevina()" )
        self.assertTrue( callable(app.endevina), "L'objecte 'endevina' de la app no és una funció" )

    def test_endevina_unitari(self):
        # test unitari
        trobat = False
        intents = 0
        # patchejem el stdin amb els numeros (monkey patch)
        # a l'arxiu hi ha els numeros del 1 al 100, ho resolem per "força bruta"
        stdin = sys.stdin
        sys.stdin = open( self.tmpfile.name , "r")
        try:
            # endevinem numero
            intents = app.endevina()
            trobat = True
        except EOFError:
            # arribem al final del fitxer i no trobem el numero
            trobat = False
        # recuperem stdin
        sys.stdin.close()
        sys.stdin = stdin
        # assert
        self.assertTrue( trobat , msg="Numero no endevinable. Ha de ser del 1 al 100 i no pot canviar a cada volta." )
        return intents

    def test_endevina_estadistic(self):
        # repetim el test molts cops per assegurar que no es fan randoms continus
        # en alguna de les 1000 iteracions hauria de fallar
        results = []
        for j in range(5):
            intents = self.test_endevina_unitari()
            results.append( intents )
            print(intents)
        # si totes les partides es resolen amb el mateix num d'intents, es que el num secret està hardcoded
        coincidencies = results.count( results[0] )
        self.assertNotEqual( coincidencies, len(results) ,
            "No pot ser sempre el mateix número({}). Ha de ser un número aleatori.".format(results[0]-1))


    def xtest_proteccio_input(self):
        # test unitari
        trobat = False
        # patchejem el stdin amb els numeros (monkey patch)
        # a l'arxiu hi ha els numeros del 1 al 100 i primer de tot un string per provocar error
        stdin = sys.stdin
        sys.stdin = open("err_nums.txt", "r")
        if True: #try:
            # endevinem numero
            app.endevina()
            trobat = True
        """except ValueError:
            trobat = False
            raise Exception("La app falla quan entres text enlloc d'un numero")
        except EOFError:
            # arribem al final del fitxer i no trobem el numero
            trobat = False"""
        # recuperem stdin
        sys.stdin.close()
        sys.stdin = stdin
        # assert
        self.assertTrue(trobat, msg="Numero no endevinable. Ha de ser del 1 al 100 i no pot canviar a cada volta.")

