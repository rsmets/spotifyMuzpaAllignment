context('Actions', () => {
    beforeEach(() => {
      // cy.visit('https://srv.muzpa.com/#/media/releases?date=2019-11-16')
    })

    it('login', () => {
        cy.visit('https://srv.muzpa.com/#/media/releases?date=2019-11-16')
        cy.get('#login').type('discodude889@gmail.com')
        cy.get('#password').type('MyMuzPa13!')
        cy.get('.rec-form-btn').click()
        cy.get('.searchfield > .ng-pristine').type('dj tennis')
        cy.get('[type="submit"]').click()
        cy.get(':nth-child(1) > ms-release-main > ms-release-main-head > ms-release-follow > .ms-release-btn').click()
        cy.get('.md-label').find('Dj Tennis')
        // cy.get('.dropdown > .button').click()
        // cy.get('.dropdown-menu-right > :nth-child(4) > a').click()
        
    })

    // it('search', () => {
    //     cy.get('.searchfield > .ng-pristine').type('dj tennis')
    //     cy.get(':nth-child(1) > ms-release-main > ms-release-main-head > ms-release-follow > .ms-release-btn').click()
    // })
})