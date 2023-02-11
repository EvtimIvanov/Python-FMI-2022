$(document).ready(function(){
    
    //Handle removing dragon from market
    $('.remove-dragon-from-market').bind('click',function(event){
        id = this.getAttribute('data-id');
        var payload = {'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()}
        $.post(`/remove_from_market/${id}`, payload, function(data){
            if(data['state']=='updated') {
                window.location.reload();
            }else {

            }
        })
    })

    //Handle adding dragon to the market
    $('.sell-dragon').bind('click',function(event){
        id = this.getAttribute('data-id');
        var payload = {'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()}
        input = document.getElementById(`price-${id}`)
        price = input.value
        
        $.post(`/add_to_market/${id}/price/${price}`, payload, function(data){
            if(data['state']=='updated') {
                window.location.reload();
            }else {
                input.style='border:red'
            }
        })
    })

    //Handle buying dragon from the market
    $('.buy-dragon').bind('click',function(event){
        id = this.getAttribute('data-id');
        var payload = {'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val()}
        $.post(`/buy_dragon/${id}`, payload, function(data){
            if(data['state']=='updated') {
                window.location.reload();
            }else {
                
            }
        })
    })

    //Handle adding dragons for breeding
    $('.add-for-breeding').bind('click', function(event){
        id = this.getAttribute('data-id');
        dragonName = document.getElementById(id).innerHTML
        firstDragon = document.getElementById('first-dragon-name')
        secondDragon = document.getElementById('second-dragon-name')
        firstDragonId = document.getElementById('dragon-id1')
        secondDragonId = document.getElementById('dragon-id2')
        if(firstDragonId.value == -1) {
            firstDragonId.value = id;
            firstDragon.innerHTML = dragonName;
        } else if(secondDragonId.value == -1){
            secondDragonId.value = id;
            secondDragon.innerHTML = dragonName;
        }

    })

    //Handle submiting the choosen dragons for breeding
    $('#submit-breed').bind('click', function(event){
        firstDragonId = document.getElementById('dragon-id1')
        secondDragonId = document.getElementById('dragon-id2')
        dragonName = document.getElementById('name-of-dragon').value

        if(firstDragonId.value != -1 && secondDragonId.value != -1) {
            var payload = {'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
             'dragon1': firstDragonId.value, 'dragon2':secondDragonId.value, 'dragon_name':dragonName}

            $.post(`/breed_dragons`, payload, function(data){
            if(data['state']=='breeded') {
                window.location.reload();
            }else {

            }
        })
    
        }
    })

    $('.return-dragon').bind('click', function(event){
        
        dragonName = this.parentElement.getElementsByTagName('p')[0];
        dragonId = this.parentElement.getElementsByTagName('input')[0];

        dragonName.innerHTML = 'Nothing choosen';
        dragonId.value = -1;
    }
    )

    $('.choose-to-fight1, .choose-to-fight2').bind('click', function(event){
        firstDragonId = document.getElementById('dragon-id1');
        firstDragonName = document.getElementById('first-dragon-name');
        secondDragonId = document.getElementById('dragon-id2');
        secondDragonName = document.getElementById('second-dragon-name');
        firstDragonClass = 'choose-to-fight1'
        id = this.getAttribute('data-id');
        currentDragonName = document.getElementById(id).innerHTML;
        if(this.classList.contains(firstDragonClass)) {
            firstDragonId.value = id;
            firstDragonName.innerHTML = currentDragonName
        } else {
            secondDragonId.value = id;
            secondDragonName.innerHTML = currentDragonName
        }
    }
    )


    //Handle submiting the choosen dragons for fight
    $('#submit-fight').bind('click', function(event){
        firstDragonId = document.getElementById('dragon-id1')
        secondDragonId = document.getElementById('dragon-id2')
        event.preventDefault()
        if(firstDragonId.value != -1 && secondDragonId.value != -1) {
            var payload = {'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
             'dragon1': firstDragonId.value, 'dragon2':secondDragonId.value}

            $.post(`/fight_dragons`, payload, function(data){
            if(data['state']=='finished') {
                winner = document.getElementById('winner')
                rounds = document.getElementById('rounds')
                stolenMoney = document.getElementById('stolen-money')

                winner.innerHTML = 'Winner is:' + data['winner-name']
                rounds.innerHTML = 'Rounds:' + data['rounds']
                stolenMoney.innerHTML = 'Stolen money:' + data['stolen-money']

            }else {

            }
        })
    
        }
    })

    $('#search-dragons').bind('input', function(event){
        let dragons = document.getElementsByClassName('dragon');
        let dragonToSearch = event.target.value.toLocaleLowerCase();
        let numberOfDragons = dragons.length;
        for(var i = 0; i < numberOfDragons; i++) {
            let nameOfDragon = dragons[i].getAttribute("name").toLocaleLowerCase()
            if(!nameOfDragon.includes(dragonToSearch)) {
                console.log("here")
                dragons[i].style.display = "none";
            } else {
                console.log("there")
                dragons[i].style.display = null;
            }
        }

    })

    $('.upgrade-stats').bind('click',function(event){
        let dragonId = document.getElementById('dragon-info').getAttribute('data-id')
        let statsName = event.target.getAttribute('stats')
        console.log(event.target.getAttribute('stats'))
        console.log(dragonId)
        event.preventDefault()
        var payload = {'csrfmiddlewaretoken': $('[name=csrfmiddlewaretoken]').val(),
            'dragonId': dragonId, 'stats': statsName}

        $.post(`update_stats`, payload, function(data){
            if(data['status']=='updated') {
                console.log("blabalba")
                window.location.reload();
            }
        })
    
        
    })
});