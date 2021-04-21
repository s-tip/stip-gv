var alchemy_config = {
    backgroundColour: "#fffff0",
    //forceLocked: true,

    nodeTypes: {"type":["Header","Indicators","Indicator","Campaign","TTPs","TTP","Incidents","Incident","Observables","Observable","Exploit_Targets","Exploit_Target",
    					"v2_identity","v2_indicator","v2_observables-data","v2_Etc_Observable","v2_IPv4_Addr_Observable","v2_File_Observable","v2_Windows_Registry_Key_Observable","v2_Domain_Name_Observable",
              "v2_malware","v2_sighting","v2_intrusion_set","v2_Threat_Actor","v2_attack_pattern","v2_Campaign","v2_CoA","v2_Report","v2_Relationship","v2_Tool","v2_Vulerability","v2_Location",
              "v2_Opinion","v2_Note","V2_CVE","v2_CustomObject", "v2_x_stip_sns", "v2_label"]},
    edgeTypes: {"type":["idref","Includes","child","Exact","Like","created_by_ref","v2_where_sighted_ref","v2_observed_data_ref","object_ref", "v2_label_ref"]},


    nodeStyle: {
        "Header": {
            "captionSize": 100,
            "captionColor": "#0000ff",
            "borderColor": "#155d6F",
            "color"  : "#2D7AA0",
            "radius": 65,
            "borderWidth" : 5,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_Report": {
            "captionSize": 100,
            "captionColor": "#0000ff",
            "borderColor": "#155d6F",
            "color"  : "#2D7AA0",
            "radius": 65,
            "borderWidth" : 5,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_x_stip_sns": {
            "captionSize": 100,
            "captionColor": "#0000ff",
            "borderColor": "#155d6F",
            "color"  : "#2D7AA0",
            "radius": 65,
            "borderWidth" : 5,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_label": {
            "captionSize": 100,
            "captionColor": "#0000ff",
            "borderColor": "#ff0000",
            "color"  : "#2D7AA0",
            "radius": 8,
            "borderWidth" : 3,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_identity": {
            "captionSize": 100,
            "captionColor": "#00ff00",
            "borderColor": "#00ff00",
            "color"  : "#2D7AA0",
            "radius": 15,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Observables": {
            "borderColor": "#A6C3FB",
            "color"  : "#A6C3FB",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_observables-data": {
            "borderColor": "#A6C3FB",
            "color"  : "#A6C3FB",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Indicators": {
            "borderColor": "#A6C3FB",
            "color"  : "#A6C3FB",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "TTPs": {
            "borderColor": "#AC71D5",
            "color"  : "#AC71D5",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Incidents": {
            "borderColor": "#FE8C3F",
            "color"  : "#FE8C3F",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Exploit_Targets": {
            "borderColor": "#626262",
            "color"  : "#626262",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Campaigns": {
            "borderColor": "#626262",
            "color"  : "#626262",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Threat_Actors": {
            "borderColor": "#626262",
            "color"  : "#626262",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_Threat_Actor": {
            "borderColor": "#626262",
            "color"  : "#626262",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Campaign": {
            "captionSize": 100,
            "captionColor": "#0000ff",
            "borderColor": "#A6C3FB",
            "color"  : "#2D7AA0",
            "radius": 10,
            "borderWidth" : 2,
            "selected": {
                "color": function() {
                  return "#FFFFFF";
                },
                "borderColor": function() {
                  return "#38DD38";
                }
              },
              "highlighted": {
                "color": function() {
                  return "#EEEEFF";
                }
              },
              "hidden": {
                "color": function() {
                  return "none";
                },
                "borderColor": function() {
                  return "none";
                }
              }
        },
        "v2_Campaign": {
            "captionSize": 100,
            "captionColor": "#0000ff",
            "borderColor": "#A6C3FB",
            "color"  : "#2D7AA0",
            "radius": 10,
            "borderWidth" : 2,
            "selected": {
                "color": function() {
                  return "#FFFFFF";
                },
                "borderColor": function() {
                  return "#38DD38";
                }
              },
              "highlighted": {
                "color": function() {
                  return "#EEEEFF";
                }
              },
              "hidden": {
                "color": function() {
                  return "none";
                },
                "borderColor": function() {
                  return "none";
                }
              }
        },
        "Courses_Of_Action": {
            "borderColor": "#626262",
            "color"  : "#626262",
            "radius": 30,
            "borderWidth" : 2,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Observable": {
            "borderColor": "#A6C3FB",
            "color"  : "#A6C3FB",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Observable_ip": {
            "borderColor": "#67FF56",
            "color"  : "#67FF56",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_IPv4_Addr_Observable": {
            "borderColor": "#67FF56",
            "color"  : "#67FF56",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Observable_domain": {
            "borderColor": "#ff6384",
            "color"  : "#ff6384",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_Domain_Name_Observable": {
            "borderColor": "#ff6384",
            "color"  : "#ff6384",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Observable_hash": {
            "borderColor": "#ffce56",
            "color"  : "#ffce56",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_File_Observable": {
            "borderColor": "#ffce56",
            "color"  : "#ffce56",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Indicator": {
            "borderColor": "#A6C3FB",
            "color"  : "#A6C3FB",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_indicator": {
            "borderColor": "#67FF56",
            "color"  : "#67FF56",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Indicator_ip": {
            "borderColor": "#67FF56",
            "color"  : "#67FF56",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Indicator_domain": {
            "borderColor": "#ff6384",
            "color"  : "#ff6384",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Indicator_hash": {
            "borderColor": "#ffce56",
            "color"  : "#ffce56",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "TTP": {
            "borderColor": "#AC71D5",
            "color"  : "#AC71D5",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Incident": {
            "borderColor": "#FE8C3F",
            "color"  : "#FE8C3F",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "Exploit_Target": {
            "borderColor": "#626262",
            "color"  : "#626262",
            "radius": 10,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
        "v2_Relationship": {
            "borderColor": "#626262",
            "color"  : "#626262",
            "radius": 5,
            "borderWidth" : 1,
            "selected": {
              "color": function() {
                return "#FFFFFF";
              },
              "borderColor": function() {
                return "#38DD38";
              }
            },
            "highlighted": {
              "color": function() {
                return "#EEEEFF";
              }
            },
            "hidden": {
              "color": function() {
                return "none";
              },
              "borderColor": function() {
                return "none";
              }
            }
        },
    },
    edgeStyle: {
        "idref": {
            "width": 1,
            "opacity": 0.8,
            "color": "#00FF00"
        },
        "created_by_ref": {
            "width": 4,
            "opacity": 0.2,
            "color": "#cccccc"
        },
        "Exact": {
            "width": 5,
            "opacity": 0.8,
            "color": "#FF0000"
        },
        "Similarity: 1": {
            "width": 5,
            "opacity": 0.8,
            "color": "#008000"
        },
        "Similarity: 2": {
            "width": 4,
            "opacity": 0.7,
            "color": "#008000"
        },
        "Similarity: 3": {
            "width": 3,
            "opacity": 0.6,
            "color": "#008000"
        },
        "Similarity: 4": {
            "width": 2,
            "opacity": 0.5,
            "color": "#008000"
        },
        "Similarity: 5": {
            "width": 1,
            "opacity": 0.4,
            "color": "#008000"
        },
        "Similarity: 6": {
            "width": 1,
            "opacity": 0.3,
            "color": "#008000"
        },
        "Similarity: 7": {
            "width": 1,
            "opacity": 0.2,
            "color": "#008000"
        },
        "Similarity: 8": {
            "width": 1,
            "opacity": 0.1,
            "color": "#008000"
        },
        "child": {
            "width": 1,
            "opacity": 0.8,
            "color": "#0000FF"
        },
        "Includes": {
            "width": 1,
            "opacity": 0.8,
            "color": "#0000FF"
        },
        "Like": {
            "width": 3,
            "opacity": 0.3,
            "color": "#FF0000"
        },
        "object_ref": {
            "width": 1,
            "opacity": 0.8,
            "color": "#0000FF"
        },
        "v2_label_ref": {
            "width": 1,
            "opacity": 0.3,
            "color": "#FF0000"
        }
    },
    clusterColors: ["#2D7AA0","#626262","#A6C3FB", "#AC71D5","#FE8C3F"],
    nodeCaptionsOnByDefault: true,
    linkDistancefn: 175,
    nodeClick: onNodeClickFunction,
    nodeCaption: nodeCaptionWithLabelFunction
};


var animationCheckboxSelector = "#animation-config-checkbox";
$(animationCheckboxSelector).change(function(){
    var isAnimate = $(this).is(':checked');
    var a = alchemy.a;
    a.conf.forceLocked = ($(this).is(':checked') != true);
    if(isAnimate == true){
        a.force.on("tick", a.layout.tick).start();
    }
});

window.onclick = function(event) {
    var modal = document.getElementById("l2-description-modal");
    if (event.target == modal) {
        $("#l2-modal-content").css("height","");
        $("#l2-description").css("overflow","auto");
        modal.style.display = "none";
    }
};

function sunitaize_encode(str){
	if (Array.isArray(str) == true){
		str = str.join(',');
	}else if(typeof(str) == 'object'){
		str = JSON.stringify(str);
	}else if(typeof(str) == 'boolean'){
		str = str.toString();
	}
	return str.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
};

function get_default_language(user_language,language_contents){
	var lang = null;
	var langs = [];
	var DEFAULT_LANG = "en";

	for (language_content in language_contents){
		langs.push(language_content);
		if (language_content == user_language){
			return language_content;
		}
	}
	
	if(langs.indexOf(DEFAULT_LANG) >= 0){
		return DEFAULT_LANG;
	}
	
	langs.sort()
	return langs[0];
};

function onNodeClickFunction(node){
    var l2_value = document.getElementById("l2-value");
    var l2_description = document.getElementById("l2-description");
    var l2_title = document.getElementById("l2-title");
    var title_text = node._properties.caption;
    var description_text = node._properties.description;
    var value_text = node._properties.value;
    var node_type = node._properties.type;
    var value_node = ["Observables","Observable","Observable_ip","Observable_domain","Observable_hash","Observable_file_name","Observable_uri","Indicators","Indicator","Indicator_ip","Indicator_domain","Indicator_hash","Indicator_uri"];

    if(title_text == null || title_text.length == 0){
        title_text = "No title";
    }

    if(description_text == null || description_text.length == 0){
        description_text = "";
    }

    if($.inArray(node_type, value_node) >= 0){
        if(value_text == null || value_text.length == 0){
            value_text = "No value";
        }
        l2_value.innerHTML = "Value: " + value_text;
    }else{
        l2_value.innerHTML = "";
    }

    l2_title.innerHTML = title_text;
    l2_description.innerHTML = description_text;
    
    var stix2_object = node._properties.stix2_object;
    var user_language = node._properties.user_language;
  	var language_contents = node._properties.language_contents;
    if (stix2_object == null){
    	$("#l2-language-options").css("display","none");
    }else{
    	var description_text = '';
    	var title_text = null;
    	var display_language = get_default_language(user_language,language_contents);
    	var display_language_content = null;
    	var original_language = 'no lang_property';
    	if(language_contents != null){
    		display_language_content = language_contents[display_language];
    	}
    	$.each(stix2_object,function(key,index){
    		if (key == "name"){
    			title_text = stix2_object[key] ;
    		}
    		if (key == "lang"){
    			original_language = stix2_object[key] ;
    		}
    		var span_key = '<span class="l2_stix2_span_key">'+ key + ':</span> ';
    		var v = stix2_object[key];
    		if(Array.isArray(v)== true){
    			v = JSON.stringify(v);
    		}else if(typeof(v) == 'object'){
    			v = JSON.stringify(v);
    		}
    		var original_v = v;
    		if (display_language_content != null){
    			if (display_language_content[key]){
    				if (Array.isArray(display_language_content[key])== true){
    					transalated_list = new Array(stix2_object[key].length);
    					$.each(display_language_content[key],function(dlc_index,list_display_value){
    						if(list_display_value.length != 0){
    							transalated_list[dlc_index] = list_display_value
    						}else{
    							transalated_list[dlc_index] = stix2_object[key][dlc_index]
    						}
    					});
    					v = JSON.stringify(transalated_list);
    				}else if(typeof(display_language_content[key])== 'object'){
    					var transalated_dict = {};
    					$.each(stix2_object[key],function(dlc_key,dict_display_value){
    						if(display_language_content[key][dlc_key]){
    							transalated_dict[dlc_key] = display_language_content[key][dlc_key];
    						}else{
    							transalated_dict[dlc_key] = dict_display_value;
    						}
    					});
    					v = JSON.stringify(transalated_dict);
    				}else{
    					v = display_language_content[key];
    				}
    			}
    		}
    		var span_value = '<span class="stix2-description" id="stix2-' + sunitaize_encode(key) + '" data-original="' + sunitaize_encode(original_v) + '">' + v + '</span><br/>\n';
    		description_text += (span_key + span_value);
    	});
    	l2_description.innerHTML = description_text;
    	if (title_text != null){
    		l2_title.innerHTML = title_text;
    	}else{
    		l2_title.innerHTML = 'A title is undefined....';
    	}
    	
    	if (language_contents == null){
            $("#l2-language-options").css("display","none");
    	}
    	else{
    		var language_options = 'Language-Options: ';
            language_options += '<a class="content-language-href" data-language= "original_content">' + original_language + ' (original)</a>, ';
            $.each(language_contents,function(language,index){
            	var content_dict = language_contents[language];
            	var anchor = '<a class="content-language-href';
            	if (display_language == language){
            		anchor += ' display-content-language-href';
            	}else{
            		anchor += ' ';
            	}
            	anchor += '" data-language="' + language + '" ';
            	$.each(content_dict,function(key,value){
            		var attr = '';
            		if(typeof(value) == 'string'){
            			attr = 'data-' + sunitaize_encode(key) + '="' + sunitaize_encode(value) + '" ';
            		}else{
            			attr = 'data-' + sunitaize_encode(key) + '="' + sunitaize_encode(JSON.stringify(value)) + '" ';
            		}
            		anchor += attr;
            	});
            	anchor += ('>' + language + '</a>,\n');
            	language_options += anchor;
            });
            language_options = language_options.slice(0,-2);
            $("#l2-language-options").html(language_options);
            $("#l2-language-options").css("display","inline");
    	}
    }

    var modal = document.getElementById("l2-description-modal");
    modal.style.display = "block";

    var before_modal_content_height = parseInt($("#l2-modal-content").css("height"));
    var alchemy_height = parseInt($("#alchemy").css("height"));

    if (before_modal_content_height > (alchemy_height / 3)){
        $("#l2-modal-content").css("height",(alchemy_height / 3) + "px");
        $("#l2-modal-content").css("overflow","scroll");
    }
};

function nodeCaptionWithLabelFunction(node){
    var avoid_redcation_node_type = ["Header","Campaign","Observables","TTPs","Incidents","Exploit_Targets"];
    var c = node.caption;
    if($.inArray(node.type,avoid_redcation_node_type) >= 0){
        return c;
    }
    if(c.length < 11){
        return c;
    }
    else{
        return c.substring(0,10) + "...";
    }
};

function nodeCaptionWithoutLabelFunction(node){
    c = node.caption;
    if(node.type=="Header"){
        return c;
    }
    return '';
};