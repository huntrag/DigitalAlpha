import Searchbar from "./searchBar1";
import AppBar from "../AppBar/index";
import { ListItem, Stack } from "@mui/material";
import "./searchBar1.css"
export default function SearchBars() {
  return (
    <>
      <AppBar />
      <Stack>
        <ListItem className="SearchBar1">
          <Searchbar />
        </ListItem>
      </Stack>
    </>
  );
}
