import { RiDeleteBinLine } from 'react-icons/ri';
import { FaHistory, FaTheaterMasks } from 'react-icons/fa';
import { GiThink, GiMaterialsScience, GiEarthAfricaEurope, GiCardRandom } from 'react-icons/gi';
import { IoMdFootball }  from 'react-icons/io';
import { IoColorPalette } from 'react-icons/io5';


function AppIcon (props) {
    let sel_icon;
    let icon_prop = {};
    for (const [key, value] of Object.entries(props)) {
        if (key !== 'sel_icon') {
            icon_prop[key] = value;
        } else {
            sel_icon = value;
        }
    }
    let icon = null;
    if (sel_icon) {
        switch (sel_icon.toLowerCase()) {
            case 'delete':          icon = RiDeleteBinLine(icon_prop);      break;
            case 'difficulty':      icon = GiThink(icon_prop);              break;
            case 'science':         icon = GiMaterialsScience(icon_prop);   break;
            case 'art':             icon = IoColorPalette(icon_prop);       break;
            case 'geography':       icon = GiEarthAfricaEurope(icon_prop);  break;
            case 'history':         icon = FaHistory(icon_prop);            break;
            case 'entertainment':   icon = FaTheaterMasks(icon_prop);       break;
            case 'sports':          icon = IoMdFootball(icon_prop);         break;
            case 'any':             icon = GiCardRandom(icon_prop);         break;
            default:                icon = null;                            break;
        }
        }
    return icon;
}

export default AppIcon;
