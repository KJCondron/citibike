
def toI( x : Any ) = x.toString.toDouble.toInt
val iids = List(305,290,464,522,2023,367)

def getStations = {

val loc = """http://www.citibikenyc.com/stations/json"""
val top = io.Source.fromURL(loc).mkString
val json = scala.util.parsing.json.JSON.parseFull(top)
val k1 = "stationBeanList"
	json match {
		case Some( m : Map[String,Any] ) => Some( m(k1).asInstanceOf[List[Any]] )          
		case _ => None
	}
	
}

def getAddresses = {

val allStations = getStations

val id = "id"
val sa = "stAddress1"
val stats = allStations.map( ss => ss.collect {
    case s : Map[String,Any] if( iids.contains( s(id) ) ) =>
        ( toI( s(id) ), s(sa) ) } )

	stats.fold( println("no stations found"))(x=>x.foreach(println))

}


def getDetails = {

val allStations = getStations

val id = "id"
val ab = "availableBikes"
val stats = allStations.map( ss => ss.collect {
    case s : Map[String,Any] if( iids.contains( s(id) ) ) =>
        ( toI( s(id) ), toI( s(ab) ) ) } )

    stats
}

def writeLnToFile( filename : String ) (text : String ) = {
    val file = new java.io.File(filename)
    val bw = new java.io.BufferedWriter(new java.io.FileWriter(file, true))
    bw.write(text)
    bw.newLine
    bw.close
}

val fl = """C:\Users\Karl\bikeStationData.txt"""
val p = writeLnToFile(fl) _

def getTime = java.util.Calendar.getInstance.getTime

def printDetails = getDetails.fold( () ) ( ss => p ( getTime + ":" + ss.toString ) )

def keepGoing( x : Int ) : Unit = {
     if ( x == 0 )
		()
	else {
	 try { printDetails }
     catch { case _ : Throwable => Unit }
     Thread.sleep(1000 * 60)
     keepGoing( if(x>0) x-1 else x )
	}
}

