import React from 'react';
import { StyleSheet, Text, View, ListView } from 'react-native';

class MyComponent extends React.Component {
  constructor() {
    super();
    const ds = new ListView.DataSource({rowHasChanged: (r1, r2) => r1 !== r2});
    this.state = {
      dataSource: ds.cloneWithRows(["1", "2", "3"])
    }
    // TODO: get this shit to update to list view dataSource
    fetch('http://localhost:8000/decks').then(function(response){
      response.json().then(function(responseJson){
        let decklist = responseJson.decks
        let deckrows = []
        for(i of decklist) {
          deckrows.push(i.name+" ["+i.num_cards+" card(s)]")
        }
        this.state = {
          dataSource:ds.cloneWithRows(deckrows)
        };
      })
    });
  }

  render() {
    return (
      <ListView
        dataSource={this.state.dataSource}
        renderRow={(rowData) => <Text>{rowData}</Text>}
      />
    );
  }
}

export default class App extends React.Component {
  render() {
    return (
      <View style={styles.container}>
        <MyComponent/>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
});
