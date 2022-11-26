import sys
import time



if __name__ == "__main__":
    input_fournisseur = "edf"  # à changer
    fournisseur = "fournisseurs."+input_fournisseur

    print(">>> Démarrage...")
    print(">>> Module sélectionné : " + input_fournisseur)

    #on importe le bon module
    try:
        from fournisseurs import edf
        print(dir(edf))

        try:
            edf.energy_login("PHILIPPE.GREGORZ@VLPM.COM", "13170Vlpm!!")
            print(">>> Connecté au fournisseurs")
        except Exception as e:
            print(e)
        else:
            try:
                edf.access_factures()
                print(">>> Page factures atteinte")
            except Exception as e:
                print(e)
            else:
                try:
                    time.sleep(4)
                    edf.download_factures()
                    print(">>> Factures téléchargées.")
                except Exception as e:
                    print(e)
    except Exception as e:
        print(e)