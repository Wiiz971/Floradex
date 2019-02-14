# Floradex
Actuellement en deuxième année de classe préparatoire aux grandes écoles (CPGE), il me faut présenter un projet appelé  TIPE (Travail d'Initiative Personnelle Encadré), en fin d'année afin d'intégrer une école d’ingénieur.  Ce projet, par le biais d'une application mobile, aiderait à identifier la flore tropicale dans la région des Caraïbes et met en avant les vertus de celle-ci. Le développement de cette application me permettrait  de rassembler des utilisateurs passionnés et des professionnels dans le domaine.

Tout d'abord, je tiens a préciser que j'utilise l'IDE Android studio


Questions :
Je ne sais pas comment mettre en relation sur une seule widget plusieurs activités.(dans mon cas, il y a le placement de la photo dans une base de données et l'envoi des données a l'application (API))
Pourquoi lorsque j'écris : val params = mCamera.getParameters(), le mCamera est souligné en rouge alors que j'ai importé android.hardware.Camera. Faut-il ajouter du Kotlin au projet ?
J'ai essayé d'importer Kotlin mais j'ai le message d'erreur suivant : org/jetbrains/kotlin/kapt/idea/KaptGradleModelorg/jetbrains/kotlin/kapt/idea/KaptGradleModel, que signifie t-il?
A celui qui si connait sur Android Studio, mon émulateur semble avoir un soucis. Il me demande de reset mon émulateur. Et lorsque que j’appuie sur le button reset, rien ne se passe....
comment envoyer des photos sur un cloud local (sur ma Raspberry Pi) avec Java. L'idée est que l'utilisateur puisse prendre un photo et que celle ci soit envoyé a ma raspberry et qu'a partir du chemin d'accès (depuis la base de données) j'envoie la photo a une API. Je suis obligé de procéder ainsi car le lien que j'envoie a l'api est de la forme "https://my-api.plantnet.org/v1/identify/all?images=http://www.lagons-plages.com/images/fleur-frangipanier.jpg&organs=flower&lang=fr&key_API";
