from owlready2 import *
import sys
import itertools

# prefix shouldn't be edited, used in queries and depends on uri of ontology
PREFIX="PREFIX fnord: <http://www.semanticweb.org/klaus/ontologies/2022/10/policeOntology1#> "

#filename of owl ontology file, should include path if not in same directory
ONTO_FILENAME="police1.owl"


#loads the ontology - must be run once before all other function calls
def loadOntology(filename=ONTO_FILENAME, path="./"):
    global onto
    #global onto_path
    #onto_path.append(path)
    onto=get_ontology(filename)
    onto.load()


# syncs the pellet resoner
def syncReasoner():
    sync_reasoner_pellet(infer_property_values = True,
                         infer_data_property_values = True)


#auxiliary function for flattening lists, used to check for existing values
def flatten(l):
    return list(itertools.chain.from_iterable(l))

# insert functions ------------------

#insert a number plate object with plateNumber nr into the ontology
def insertNumberPlate(nr="ABC123"):
    if nr in flatten(getAllNumberPlates()):
        sys.stderr.write("Number plate {} already exists".format(nr))
        return
    
    with onto:
        q=default_world.sparql(PREFIX+"""
        INSERT { ?uri rdf:type fnord:NumberPlate .
            ?uri fnord:plateNumber \""""+nr+"""\".}
        WHERE { BIND (UUID() AS ?uri) }
        """)
    return q

def insertPerson(persID, name="Kjell Kriminell"):
    if str(persID) in flatten(getAllPersons()):
        sys.stderr.write("Person With ID {} already exists".format(persID))
        return
    with onto:
        q=default_world.sparql(PREFIX+"""
        INSERT { ?uri rdf:type fnord:Person .
            ?uri fnord:hasPersonID \""""+str(persID)+"""\".
            ?uri fnord:hasPersonName \""""+name+"""\".}
        WHERE { BIND (UUID() AS ?uri) }
        """)
        return q



#sets number plate with plateNumber nr as the current number plate
#use insertNumberPlate() first to create a number plate entity with the
# desired registration number
# Also doen't remove any previously selected plates from being the
# one currently scanned, because I can't get the DELETE statement to work
def setCurrentNumberPlate(nr="AAA111"):
    #todo: remove other instances of CurrentlyScannedNumberPlate ?
    with onto:
        s=PREFIX + """
            INSERT { ?plate rdf:type fnord:CurrentlyScannedNumberPlate .}
            WHERE { ?plate fnord:plateNumber \""""+nr+"""\" .}
            """
        q=default_world.sparql(s)
    return q


# TODO: insert methods for vehicle reg, crime records, asp


# get functions ------------------

def getAllPersons():
    with onto:
        q = list(default_world.sparql(PREFIX+
            """SELECT ?id ?name
            WHERE {?person rdf:type fnord:Person.
                ?person fnord:hasPersonID ?id.
                ?person fnord:hasPersonName ?name} """))
        return q
    
def getAllNumberPlates():
    with onto:
        q = list(default_world.sparql(PREFIX+
            """SELECT ?n
            WHERE {?p rdf:type fnord:NumberPlate.
                ?p fnord:plateNumber ?n} """))
        return q



def get_Human_Aware_Planning_session_modifiers():
    """
    Returns a dictionary object with session modifiers to proactively
    anticipate user needs, because human aware planning is serious business
    """
    session_settings={}

    #search each attribute in individual queries, because nothing
    #is returned if some attribute is missing
    #should be a better way of doing this, but can't be bothered to
    #find out how
    with onto:
        q1=list(default_world.sparql(PREFIX+"""
            SELECT ?lang
            WHERE {?s rdf:type fnord:HAP_Current_Session .
            ?s fnord:HAP_session_language ?l .
            ?l fnord:HAP_lang_langName ?lang .
            }"""))
        if q1:
            session_settings["Language"]=flatten(q1)

        q2=list(default_world.sparql(PREFIX+"""
            SELECT ?volume
            WHERE {?s rdf:type fnord:HAP_Current_Session .
            ?s fnord:HAP_session_audio_volume ?vol .
            ?vol fnord:HAP_state_to_string ?volume .
            }"""))
        if q2:
            session_settings["volume"]=flatten(q2)

        q3=list(default_world.sparql(PREFIX+"""
            SELECT ?brightness
            WHERE {?s rdf:type fnord:HAP_Current_Session .
            ?s fnord:HAP_session_screen_brightness ?br .
            ?br fnord:HAP_state_to_string ?brightness .
            }"""))
        if q3:
            session_settings["screen brightness"]=flatten(q3)

        q4=list(default_world.sparql(PREFIX+"""
            SELECT ?audio
            WHERE {?s rdf:type fnord:HAP_Current_Session .
            ?s fnord:HAP_session_background_audio ?audio .
            }"""))
        if q4:
            session_settings["background audio"]=flatten(q4)

        q5=list(default_world.sparql(PREFIX+"""
            SELECT ?sub
            WHERE {?s rdf:type fnord:HAP_Current_Session .
            ?s fnord:HAP_session_use_subtitles ?sub .
            }"""))
        if q5:
            session_settings["subtitles"]=flatten(q5)           

        q6=list(default_world.sparql(PREFIX+"""
            SELECT ?contr
            WHERE {?s rdf:type fnord:HAP_Current_Session .
            ?s fnord:HAP_session_use_high_contrast_gui ?contr .
            }"""))
        if q6:
            session_settings["high contrast gui"]=flatten(q6)

        
        q7=list(default_world.sparql(PREFIX+"""
            SELECT ?t2s
            WHERE {?s rdf:type fnord:HAP_Current_Session .
            ?s fnord:HAP_session_use_text-to-speech_gui ?t2s .
            }"""))
        if q7:
            session_settings["text-to-speech"]=flatten(q7)  
        
    return session_settings




def getCurrentNumberPlate():
    s=PREFIX+"""
        SELECT ?plate ?number
        WHERE {?plate rdf:type fnord:CurrentlyScannedNumberPlate.
         ?plate fnord:plateNumber ?number .}
        """
    with onto:
        q=default_world.sparql(s)
    return list(q)


def getNumberPlateThreatLevels(nr="ABC123"):
    s=PREFIX+"""
        SELECT ?tl ?notes WHERE{
            ?plate rdf:type fnord:CurrentlyScannedNumberPlate .
            ?plate fnord:plateNumber \""""+nr+"""\"
            ?plate fnord:plateThreatLevel ?tl .
            ?plate fnord:plateNotes ?notes.
        }
    """
    with onto:
        q = default_world.sparql(s)
    return list(q)

#returns the criminal record threat estimates of the
# driver of the currently scanned numberplate
def getCriminalRecordThreatEstimate(nr="ABC123"):
    s = PREFIX + """ SELECT ?e WHERE{
        ?record fnord:hasPlateNumber \""""+nr+"""\"
        ?record fnord:hasRegisteredOwner ?person
        ?person rdf:type fnord:PersonToBeChecked .
        ?person fnord:criminalRecordThreatEstimate ?e

    }"""
    with onto:
        q = default_world.sparql(s)
    return list(q)

#appears not to work for some raeson
# perhaps we can find a way to work around this
def clearCurrentNumberPlate():
    s=PREFIX+"""
        DELETE {?plate rdf:type fnord:CurrentlyScannedNumberPlate .}
        WHERE  {?plate rdf:type fnord:CurrentlyScannedNumberPlate .}
    """
    with onto:
        default_world.sparql(s)




#for debugging

def getAllTriples():
    with onto:
        q=default_world.sparql("""SELECT * WHERE {
            ?subject ?predicate ?object . }""")
    return list(q)

def writeAllTriples(filename="triples.txt"):
    q=getAllTriples()
    f=open(filename, mode='w')
    for t in q:
        f.write(str(t)+"\n")
    f.close()



def main():

    print("loading ontology")
    loadOntology()
    
    print("Currently assigned number plate:")
    q=getCurrentNumberPlate()
    print(q)

    print("Assigning number plate ABC123")
    setCurrentNumberPlate("ABC123")


    print("Shows thatn number plate is now assigned:")
    q=getCurrentNumberPlate()
    print(q)

        
    print("Getting number plate threat levels")
    q=getNumberPlateThreatLevels("ABC123")
    print(q)
    
    print("rNothing, so need to run reasoner fist")
    syncReasoner()

    print("Show that number plate threat levels have been derived:")
    q=getNumberPlateThreatLevels()
    print(q)

    print("Assign number plate XYZ789")
    print("(This doesn't remove previously assigned plates because I cant"+
          "get DELETE statements to work)")
    setCurrentNumberPlate("XYZ789")

    print("Currently assigned number plate:")
    q=getCurrentNumberPlate()
    print(q)

    print("Get criminal record threat estimate from XYZ789")
    q=getCriminalRecordThreatEstimate("XYZ789")
    print(q)

    print("First, need to run reasoner again")
    syncReasoner()

    print("Get criminal record threat estimate from XYZ789")
    q=getCriminalRecordThreatEstimate("XYZ789")
    print(q)

    print("Get criminal record threat estimate from ABC123"+
          " (Shouldn't exist)")
    q=getCriminalRecordThreatEstimate("ABC123")
    print(q)

    print("Get session modifiers to proactively address user need using"+
          " Human Aware Planning:")
    q=get_Human_Aware_Planning_session_modifiers()
    print(q)

#............................................

#main()
