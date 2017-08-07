
$(function() {
	AuctionBrowse.initialize();
});

var AuctionBrowse = {

	/**
	 * Initialize all the form elements.
	 *
	 * @constructor
	 */
	initialize: function() {
		$('#browse-form').submit(AuctionBrowse.submit);
		$('.results-per-page').change(AuctionBrowse.resultsPerPage);

		// Bind events
		$('.browse-categories .tier1').find('select').change(function() {
			AuctionBrowse.resetTiers([2, 3], true);
			AuctionBrowse.selectTier(1, this.value);
		});

		$('.browse-categories .tier2').find('select').change(function() {
			AuctionBrowse.resetTiers([3], true);
			AuctionBrowse.selectTier(2, this.value);
		});

		$('.browse-categories .tier3').find('select').change(function() {
			AuctionBrowse.selectTier(3, this.value);
		});

		// Numeric values only
		$('#minLvl, #maxLvl').blur(function() {
			this.value = Core.numeric(this.value);
		});

		// Preselect filters
		var filters = $('#filter-id').val();

		if (filters && filters != '-1') {
			filters = filters.split(',');

			AuctionBrowse.tier1 = filters[0];
			AuctionBrowse.showTier(1, -1, filters[0]);

			AuctionBrowse.tier2 = filters[1] || null;
			AuctionBrowse.showTier(2, filters[0], filters[1] || '');
			
			if (filters.length > 1) {
				AuctionBrowse.tier3 = filters[2] || null;
				AuctionBrowse.showTier(3, filters[1] || -1, filters[2] || '');
			}
		}

		// Bind sorting
		$('.auction-house .table thead th a').click(function() {
			AuctionBrowse.saveLast($(this).attr('href'));
		});
	},

	/**
	 * Chosen categories.
	 */
	tier1: null,
	tier2: null,
	tier3: null,

	/**
	 * Resets the tier wrapper by disabling all selects and hiding them.
	 *
	 * @param tiers
	 * @param showDefault
	 */
	resetTiers: function(tiers, showDefault) {
		if (tiers.length > 0) {
			var length = tiers.length - 1;

			for (var i = 0; i <= length; ++i) {
				var tier = tiers[i];

				$('.browse-categories .tier'+ tier).find('select')
					.attr('disabled', 'disabled')
					.addClass('disabled')
					.hide();

				AuctionBrowse['tier'+ tier] = "";

				if (showDefault)
					$('#tier'+ tier +'_-1').show();
			}
		}
	},

	/**
	 * Save the selected tier value and open up the next tier if it exists.
	 *
	 * @param tier
	 * @param value
	 */
	selectTier: function(tier, value) {
		AuctionBrowse['tier'+ tier] = value;

		var nextTier = tier + 1;

		// Does next tier exist?
		if (value >= 0 && document.getElementById('tier'+ nextTier +'_'+ value))
			AuctionBrowse.showTier(nextTier, value);
	},

	/**
	 * Display the tier and hide the default option.
	 *
	 * @param tier
	 * @param id
	 * @param value
	 */
	showTier: function(tier, id, value) {
		value = value || -1;
		
		var empty = $('#tier'+ tier +'_-1');
		var select = $('#tier'+ tier +'_'+ id);

		if (select.length) {
			empty.hide();

			select
				.removeAttr('disabled')
				.removeClass('disabled')
				.show()
				.val(value);
				
		} else {
			empty.show();
		}
	},

	/**
	 * Empty all the hidden form inputs and reset the category dropdowns.
	 */
	reset: function() {
		$('#itemName, #minLvl, #maxLvl').val("");
		$('#tier1_-1').val(-1);
		$('#itemRarity').val(0);

		AuctionBrowse.tier1 = -1;
		AuctionBrowse.resetTiers([2, 3], true);

		Cookie.erase('wow.auction.lastBrowse');
	},

	/**
	 * Results per page.
	 */
	perPage: 20,

	/**
	 * Change the start/end values and submit the form.
	 */
	resultsPerPage: function() {
		AuctionBrowse.perPage = $(this).val();

		$('#browse-form').submit();
	},

	/**
	 * Merge the category tier IDs into a single value before submitting.
	 */
	submit: function() {
		var filter = '-1';

		if (AuctionBrowse.tier1) {
			filter = AuctionBrowse.tier1;

			if (AuctionBrowse.tier2 && AuctionBrowse.tier2 != '-1') {
				filter += ','+ AuctionBrowse.tier2;

				if (AuctionBrowse.tier3 && AuctionBrowse.tier3 != '-1')
					filter += ','+ AuctionBrowse.tier3;
			}
		}

		$('#filter-id').val(filter);

		// Reset to page 1 on submit
		$('#startNo').val('');
		$('#endNo').val(AuctionBrowse.perPage);

		var fields = ['minLvl', 'maxLvl', 'startNo', 'endNo'],
			length = (fields.length - 1),
			name = $('#itemName').val(),
			nameOld = $('#itemNameOld').val();

		for (var i = 0, field; i <= length; ++i) {
			field = $('#'+ fields[i]);

			if ((name != nameOld && nameOld != '') || (field.val() == "") || isNaN(field.val())) {
				if (fields[i] == 'endNo')
					field.val('20');
				else if (fields[i] == 'startNo')
					field.val('0');
				else
					field.val('-1');
			}
		}

		AuctionBrowse.saveLast();
		return true;
	},

	/**
	 * Save the last search to a cookie.
	 *
	 * @param query
	 */
	saveLast: function(query) {
		if (query === undefined)
			query = '?'+ $('#browse-form').serialize();

		Cookie.create('wow.auction.lastBrowse', query);
	}

};